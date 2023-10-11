import olefile
import pandas as pd
f = olefile.OleFileIO('hwp\보고서.hwp')
#PrvText 스트림 내의 내용을 읽기
encoded_text = f.openstream('PrvText').read() 
#인코딩된 텍스트를 UTF-16으로 디코딩
decoded_text = encoded_text.decode('UTF-16').replace('>', '').replace('\r\n', '').split('<')

df = pd.DataFrame(decoded_text, columns=['contents'])

for i in df.index:
    print(df.loc[i, 'contents'])