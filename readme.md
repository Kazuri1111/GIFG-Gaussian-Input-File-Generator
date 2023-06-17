# GIFG-Gaussian-Input-File-Generator

化合物名、またはsmilesからgaussianのgjfファイルを生成するpythonスクリプト

## 概要

pubchempyとrdkitを使って、化合物の名称(英語)またはsmilesからgaussianのインプットファイル(gjf)を生成するpythonスクリプトです。コマンドライン引数を指定することで、cpuのコア数、計算方法などを記述したファイルを生成することもできます。MMFFで租最適化した後、XYZ座標を生成します。

## 使い方

python gifg.pyの後に各種引数を指定して実行してください。gifg.py --helpとすることでヘルプを見ることが出来ます。

●requirements

・python(3.10.11で動作確認済み)<br>
・rdkit<br>
・pubchempy<br>
・argparse<br>
・pandas<br>  

●引数の一覧

--name: 化合物名<br>
--smiles: smiles<br>
--chk: link0に記述するchkファイル名(拡張子.chkを含めずに入力する デフォルト："chk")<br>
--out: 生成するgjfファイルのファイル名(拡張子.gjfを含めずに入力する デフォルト："out")<br>
--cpu, --mem: link0に記述するNprocSharedとmemの値 (デフォルト：それぞれ"6"と"1GB")<br>
--method: 計算条件(例："opt B3LYP/6-31g(d)")<br>
--title: タイトル(デフォルト:"title)<br>
--charge: 分子の電荷(デフォルト："0")<br>
--multiplicity: 分子の多重度(デフォルト:"1")<br>
いずれも必須ではありませんが、--nameと--smilesのどちらか一方のみを必ず指定してください。<br>
--nameを指定したとき、--chkと--outと--titleを指定しなければ、すべて--nameと同じ値になります。<br>  

## 注意点

・生成時に同名のファイルが既に存在する場合は、警告なしで上書きされます。--outの値が既存のファイルと被っていないか、確認してから実行してください。<br>
・linuxで実行される場合、--methodの内容にかっこが含まれているとうまく動作しないときがあります。引用符で内容をくくって実行することを推奨します。  

## 謝辞

hodakam氏がZenn上で公開されていたコードを参考に作成しました。感謝します。
<https://zenn.dev/hodakam/articles/09462ab3abb22e>
