from binascii import hexlify
import re
import wave
from collections import OrderedDict
import os
import glob

def check_voicepeak_voice(text:str) -> str:
    """
    voicepeakの音声の種類を取得する
    params:
        text: チェックしたいテキスト
    """
    return text.split("-")[1]
    
def text2hex_str(text:str) -> str:
    """
    テキストをUTF-16でエンコードして16進数文字列に変換する
    params:
        text: 変換したいテキスト
    """
    text_in_utf16 = hexlify(text.encode('utf-16'))
    hex_str = text_in_utf16.decode("ascii")[4:]
    return hex_str

def text2exo_str(text:str) -> str:
    """
    テキストをexoファイルの書式に変換する
    params:
        text: 変換したいテキスト
    """
    hex_str = text2hex_str(text)
    zero_count = 4096-len(hex_str)
    hex_str += "0"*zero_count
    return hex_str

def hex_str2text(hex_str:str) -> str:
    """
    16進数文字列をUTF-16でデコードしてテキストに変換する
    params:
        hex_str: 変換したい16進数文字列
    """
    byte_string = bytes.fromhex(hex_str)
    return byte_string.decode("utf-16").replace("\x00","")


class AviutlObjects:
    """
    Aviutl上の長方形のオブジェクト一つの情報に対応するクラス
    """
    def __init__(self,section_name):
        """
        sectionはexoファイル上の[0.1]の左側の数字
        subsectionはexoファイル上の[0.1]の右側の数字
        params:
            section_name: オブジェクトのセクション名
        """
        self.section_name = section_name
        self.info = OrderedDict()
    
    def add_items(self, section:str, key:str, value: str):
        self.info[section] = self.info.get(section,OrderedDict())
        self.info[section][key] = value
    
    def get_exo_format(self):
        """
        exoファイルの書式を取得する
        """
        ret_str = ""
        if self.section_name == "exedit":
            ret_str += "[exedit]\n"
            for key,value in self.info["init"].items():
                ret_str += key + "=" + value + "\n"
        else:
            
            for key,value in self.info.items():
                if key == "init":
                    ret_str += "[" + self.section_name + "]\n"
                else:
                    ret_str += "[" + self.section_name + "." + key + "]\n"
                for key2,value2 in value.items():
                    ret_str += key2 + "=" + value2 + "\n"
           
        return ret_str
    
    def __getitem__(self,key):
        return self.info[key]
    
    def __str__(self):
        return str(self.info)

if __name__ == "__main__":
    dic = {}
    with open("config.txt","r",encoding="utf-8") as f:
        for i in f:
            i = i.strip()
            temp = i.split("=")
            dic[temp[0]] = temp[1]

    exo_path = dic["exo_path"]
    voicepeak_output_path = dic["voicepeak_output_path"]
    wait_frame = int(dic["wait_frame"]) #音声と音声の間に開けるフレーム数
    objects = []

    #テンプレートのexoファイルの情報を読み込む
    with open(exo_path, "r",encoding="shift-jis") as f:
        section_info = None
        section_pattern = r"\[\d+\]"
        subsection_pattern = r"\[\d+\.\d+\]"
        section_number = "" #現在のセクション番号
        subsection_number = "" #現在のサブセクション番号
        aviutl_object = None
        for i in f:
            i = i.strip()
            section_match = re.search(section_pattern, i)
            subsection_match = re.search(subsection_pattern, i)
            if section_match:
                if aviutl_object:
                    objects.append(aviutl_object)
                section_number = section_match.group()[1:-1]
                subsection_number = ""
                aviutl_object = AviutlObjects(section_number)
            elif subsection_match:
                subsection_number = subsection_match.group()[1:-1].split(".")[1]
            elif i == "[exedit]":
                aviutl_object = AviutlObjects("exedit")
            else:
                if subsection_number == "":
                    aviutl_object.add_items("init",i.split("=")[0],i.split("=")[1])
                else:
                    aviutl_object.add_items(subsection_number,i.split("=")[0],i.split("=")[1])
        else:
            if aviutl_object:
                objects.append(aviutl_object)

    #voicepeakの音声に対応するテキストオブジェクトを抽出
    exedit_object = None #exeeditのオブジェクトを保存する
    audio_object = None #音声のオブジェクトを保存する
    voicepeak_objects = {} #voicepeakの音声に対応するAviutlオブジェクトが保存される辞書
    for i in objects:
        if i.section_name == "exedit":#exeditセクションのみ先に出力
           exedit_object = i
           continue

        if i["0"]["_name"] == "テキスト" :
            voicepeak_objects[hex_str2text(i["0"]["text"])] = i
        elif i["0"]["_name"] == "音声ファイル":
            audio_object = i
        else:
            pass


    #voicepeak出力の音声とテキストデータを取得
    audio_paths = glob.glob(os.path.join(voicepeak_output_path,"*.wav"))
    txt_paths = glob.glob(os.path.join(voicepeak_output_path,"*.txt"))
    assert len(audio_paths) == len(txt_paths), "音声ファイルとテキストファイルの数が一致しません"


    #exoファイルの生成
    exo_outputs = "" #最終的にexoファイルに出力する文字列
    start = 1
    section_number = 0
    audio_paths.sort(reverse=False)
    txt_paths.sort(reverse=False)
    exo_outputs += exedit_object.get_exo_format()
    for audio_path,txt_path in zip(audio_paths,txt_paths):
        audio_path = os.path.abspath(audio_path)
        voice_type = check_voicepeak_voice(audio_path)
        with wave.open(audio_path, "rb") as wr:
            fr = wr.getframerate()
            fn = wr.getnframes()
        frame_length = int(fn/fr*int(exedit_object["init"]["rate"]))
        if voice_type in voicepeak_objects.keys():
            aviutl_object = voicepeak_objects[voice_type]
        else:
            raise Exception("テンプレートのexoファイルに、{}の設定テキストオブジェクトが存在しません".format(voice_type))
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        

        #音声オブジェクトの設定
        if audio_object:
            audio_object.section_name = str(section_number)
            audio_object["0"]["file"] = audio_path
            audio_object["init"]["start"] = str(start)
            audio_object["0"]["動画ファイルと連携"]=str(0)
            audio_object["init"]["end"] = str(start + frame_length)
            audio_object["init"]["layer"] = str(1)
            exo_outputs += audio_object.get_exo_format()
            section_number += 1
        else:
            raise Exception("テンプレートのexoファイルに音声オブジェクトがありません")

        #テキストオブジェクトの設定
        aviutl_object.section_name = str(section_number)
        aviutl_object["0"]["text"] = text2exo_str(text)
        aviutl_object["init"]["start"] = str(start)
        aviutl_object["init"]["end"] = str(start + frame_length)
        aviutl_object["init"]["layer"] = str(2)
        exo_outputs += aviutl_object.get_exo_format()
        section_number += 1

        start += frame_length + wait_frame
        
        

    with open("output.exo","w",encoding="shift-jis") as f:
        f.write(exo_outputs)
    

