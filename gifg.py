# ref: https://zenn.dev/hodakam/articles/09462ab3abb22e

# 各種パッケージのimport
from rdkit import Chem
from rdkit.Chem import AllChem
import pandas as pd
import argparse
import pubchempy

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="gjf generator Ver. 0.0.1")
parser.add_argument("--name")
parser.add_argument("--smiles")
parser.add_argument("--chk", default="chk", help="chk filename(without extension)")
parser.add_argument(
    "--out", default="out", help="output gjf filename(without extension)"
)
parser.add_argument("--cpu", default="6")
parser.add_argument("--mem", default="1GB")
parser.add_argument("--method", nargs="*", default="")
parser.add_argument("--title", nargs="*", default="title")
parser.add_argument("--charge", default="0")
parser.add_argument("--multiplicity", default="1")
args = parser.parse_args()

# 引数でnameが与えられた時の処理
if args.name:
    # pubchemからCanonicalSMILESを取得
    smiles_list = pubchempy.get_properties(["CanonicalSMILES"], args.name, "name")
    smiles = smiles_list[0]["CanonicalSMILES"]
    if smiles:
        args.smiles = smiles
    else:
        print("API Error")
        exit()

    # chk,out,titleの引数がデフォルトの時に化合物名で上書きする
    if args.chk == "chk":
        args.chk = args.name
    if args.out == "out":
        args.out = args.name
    if args.title == "title":
        args.title = args.name

# method,titleの引数にスペースが含まれる場合の処理(ただし、クオーテーションでくくることを推奨)
if type(args.method) == list:
    args.method = " ".join(args.method)
if type(args.title) == list:
    args.title = " ".join(args.title)

# smilesから分子を生成、MMFFで租最適化
mol = Chem.MolFromSmiles(args.smiles)
mol = Chem.AddHs(mol)
etkdg = AllChem.ETKDG()
AllChem.EmbedMolecule(mol, etkdg)
AllChem.MMFFOptimizeMolecule(mol)

# 各原子の座標のリストを作成
elements = [atom.GetSymbol() for atom in mol.GetAtoms()]
for c in mol.GetConformers():
    positions = c.GetPositions()

atoms = pd.DataFrame(columns=["element", "x", "y", "z"])
atoms["element"] = elements
atoms["x"] = positions[:, 0]
atoms["y"] = positions[:, 1]
atoms["z"] = positions[:, 2]

# Input fileを生成
header = f"""%chk={args.chk}.chk
%NprocShared={args.cpu}
%Mem={args.mem}
#{args.method}

{args.title}

{args.charge} {args.multiplicity}

"""

# 生成したものの書き込み
header = "\n".join(header.splitlines())
with open(f"{args.out}.gjf", "w", encoding="ascii") as f:
    f.write(header)
    for v in atoms.values:
        f.write(" ".join(map(str, v)) + "\n")
    f.write("\n")
    print(f"Generated input file: {args.out}.gjf")
