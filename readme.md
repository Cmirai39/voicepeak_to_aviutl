# voicepeak_to_aviutlの使い方
voicepeak_to_aviutlはvoicepeakで出力した音声から、Aviutl上での字幕を自動で生成するプログラムとなっています。

動画での説明:https://www.youtube.com/watch?v=e59-W6Yh1Hs
## テンプレートexoの作成
まずはじめにAviutlで新規プロジェクトを作成してください。その際の解像度などは、作る動画のものを設定してください。
そして、場所はどこでも構いませんが、テキストオブジェクトを作成してください。その際にテキスト部分に"女性1"や"男性2"など、Voicepeakでの音声の種別を入力してください。"女性1"とテキスト部分に入力したオブジェクトは"女性1"の字幕のテンプレートとなります。文字色や場所、サイズなどをお好みで調節してください。そして、動画で使う音声種別に対してすべてテキストオブジェクトを作成し終えたら、最後に空の音声オブジェクトを作成してください。これの音量などを変更することで、字幕自動生成の際の音声の音量などを調整することができます。

上記のファイルを作成し終えたら、拡張編集上の何もオブジェクトがないところで右クリックし、"ファイル>オブジェクトファイルのエクスポート"を選択してください。これにより、テンプレートとなるexoファイルを作成することができます。ここでは、template.exoファイルを出力したとします。

## voicepeakで音声を出力する
voicepeakで音声を出力する際には、少し手順が必要になります。まずは、出力したい音声ファイルがあるプロジェクトで"ファイル>出力"を選択してください。すると、出力設定のwindowが表示されると思います。このとき、フォーマットは.wav、セリフをファイルに保存をオン、ブロックごとに分割して保存をオン、命名規則を最初に番号、次にナレーター名に設定してください。この設定で音声ファイルを出力します。ここでは、音声フォルダに出力したとします。

![alt text](image/voicepeak_setting.png)

## 音声と字幕のAviutlのデータを作成する
voicepeak_to_aviutl.exeとconfig.txtを同じフォルダに入れてください。
そして、先ほどまでの手順で作成したtemplate.exoと音声データのフォルダも同じフォルダ内にいれます。
フォルダ構造を以下のようにしてください。
 - 音声
    - 01-女性1-任意の名前.wav
    - 01-女性1-任意の名前.txt
    - ...
 - template.exo
 - config.txt
 - voicepeak_to_aviutl.exe

次に, config.txtの中身を変更していきます。
exo_pathはテンプレートとなるexoファイルのパスを表しています。今回はexo_path=template.exoとなっています。
次に、voicepeak_output_pathはvoicepeakが出力した音声データのフォルダパスを表しています。ここではvoicepeark_output_path=音声となっています。最後にwait_frameは前の音声と次の音声の間隔をどれだけあけるか(フレーム数で指定)を指定することができます。特にそのままで問題ないと思います。

ここまで準備が完了したら、voicepeak_to_aviutl.exeをダブルクリックしてください。output.exoが生成されたら成功です。あとはAviutlの拡張編集上で何もないところで、"ファイル>オブジェクトファイルのインポート"をクリックするか、exoファイルを拡張編集上にD&Dすれば、字幕と音声が読み込まれるはずです。

## 免責事項
本ツール作成者は、本ツールを利用したことにより生じた利用者の損害及び利用者が第三者に与えた損害に関して、一切の責任を負いません。
