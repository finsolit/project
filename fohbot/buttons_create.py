

def buttons(buttons_str):
    buttons_string=buttons_str.replace('\n',' ')
    buttons_string+=' '
    button_url=''
    button_name_was=0
    button_rp=0
    array1=[]
    array2=[]
    for i in range(0,len(buttons_string)):
        if buttons_string[i]=='-':
            if buttons_string[i-1]==' ':
                button_name=buttons_string[button_rp:i-1] 
                button_name_was=1			
            else:
                button_name=buttons_string[button_rp:i]
                button_name_was=1
            button_rp=i+1
            if 	buttons_string[i+1]==' ':
                button_rp+=1
        if i<= button_rp:
            continue	
        if button_name_was==1 and 	buttons_string[i]==' ':
            print('nashel url',i,button_rp)
            button_url=buttons_string[button_rp:i]
            button_name_was=0
            print(button_name)
            print(button_url)
            array1.append(button_name)
            array2.append(button_url)
            button_rp=i+1
    resp=[]
    resp.append(array1)
    resp.append(array2)
    return(resp)