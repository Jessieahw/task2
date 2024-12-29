import csv
import requests
import re
import os
import glob
def parse(file1, file2):
    hand=open(file1)
    IDENTITY=""
    for line in hand:
        line=line.strip()
        if re.findall('^COMPANY CONFORMED NAME:',line):
            k = line.find(':')
            comnam=line[k+1:]
            comnam=comnam.strip()
            IDENTITY='<HEADER>\nCOMPANY NAME: '+str(comnam)+'\n'                                         
            break
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^CENTRAL INDEX KEY:',line):
            k = line.find(':')
            cik=line[k+1:]
            cik=cik.strip()
            IDENTITY=IDENTITY+'CIK: '+str(cik)+'\n'
            break
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^STANDARD INDUSTRIAL CLASSIFICATION:',line):
            k = line.find(':')
            sic=line[k+1:]
            sic=sic.strip()
            siccode=[]
            for s in sic: 
                if s.isdigit():
                    siccode.append(s)    
            IDENTITY=IDENTITY+'SIC: '+''.join(siccode)+'\n'
            break
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^CONFORMED SUBMISSION TYPE:',line):
            k = line.find(':')
            subtype=line[k+1:]
            subtype=subtype.strip()
            IDENTITY=IDENTITY+'FORM TYPE: '+str(subtype)+'\n'
            break
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^CONFORMED PERIOD OF REPORT:',line):
            k = line.find(':')
            cper=line[k+1:]
            cper=cper.strip()
            IDENTITY=IDENTITY+'REPORT PERIOD END DATE: '+str(cper)+'\n'
            break
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^FILED AS OF DATE:',line):
            k = line.find(':')
            fdate=line[k+1:]
            fdate=fdate.strip()                        
            IDENTITY=IDENTITY+'FILE DATE: '+str(fdate)+'\n'+'</HEADER>\n'
            break  
    content=hand.read()
    IDENTITY += content
    with open(file2, 'a') as f:
        f.write(str(IDENTITY))
        f.close()
    hand.close()
def headerclean(temp, temp1):
    mark0=0
    strings1=['</SEC-HEADER>','</IMS-HEADER>']
    hand=open(temp)
    hand.seek(0)
    for x, line in enumerate(hand):
        line=line.strip()
        if any(s in line for s in strings1):
            mark0=x
            break
    hand.seek(0)
    newfile=open(temp1,'w')
    for x, line in enumerate(hand):
        if x>mark0:
            newfile.write(line)
    hand.close()
    newfile.close()
    newfile=open(temp1,'r')
    hand=open(temp,'w')        
    for line in newfile:
        if "END PRIVACY-ENHANCED MESSAGE" not in line:
            hand.write(line)                
    hand.close()                
    newfile.close()
def xbrl_clean(cond1, cond2, str0):
    locations=[0]
    #print locations
    placement1=[]
    str0=str0.lower()
    for m in re.finditer(cond1, str0):
        a=m.start()
        placement1.append(a)
    if placement1!=[]:
        placement2=[]
        for m in re.finditer(cond2, str0):
            a=m.end()
            placement2.append(a)
        len1=len(placement1)
        placement1.append(len(str0))

        


        for i in range(len1):
            placement3=[]
            locations.append(placement1[i])
            for j in placement2:
                if (j>placement1[i] and j<placement1[i+1]):
                    placement3.append(j)
                    break
            if placement3!=[]:
                locations.append(placement3[0])
            else:
                locations.append(placement1[i])
        # here
        # if len(placement1) != len(placement2):
        #     raise ValueError("Mismatched <xbrl> tags: check input data.")

    return locations
def table_clean(cond1, cond2, str1):
    Items0=["item 1", "item1", "item1a", "item 1a"]
    Items1=["item 7", "item 8","item 2","item 3","item 4","item 5","item 6","item 9", "item 10", "item7","item8" "item2","item3","item4","item5","item6","item9", "item10"]
    str2=str1.lower()
    str2 = str1.lower().replace("&nbsp;", " ").replace("&NBSP;", " ")
    
    # Ensure that HTML entities and extra spaces are cleaned up
    str2 = re.sub(r'&#\d{1,5};', '', str2)  # Remove HTML numeric entities
    str2 = re.sub(r'&#.{1,5};', '', str2)
    placement1=[]
    for m in re.finditer(cond1, str2):
        a=m.start()
        placement1.append(a)
    n=len(placement1)
    placement1.append(len(str2))
    placement2=[]
    for m in re.finditer(cond2, str2):
        a=m.end()
        placement2.append(a)
    if (placement1!=[] and placement2!=[]):
        current=str1[0:placement1[0]]
        for i in range(n):
            begin=placement1[i]
            for j in placement2:
                if j>begin:
                    end=j
                    break
            if end=="":
                current=current+str1[begin:placement1[i+1]]
            else:
                str2=""
                str2=str1[begin:end].lower()
                str2=str2.replace("&nbsp;"," ")
                str2=str2.replace("&NBSP;"," ")
                p = re.compile(r'&#\d{1,5};')
                str2=p.sub("",str2)
                p = re.compile(r'&#.{1,5};')
                str2=p.sub("",str2)
                if any(s in str2 for s in Items0):
                    if not any(s in str2 for s in Items1):
                        current=current+str2
                current=current+str1[end:placement1[i+1]]
                end=""
    else:
        current=str1
    return current

filepath="/Users/jessie/Downloads/task2/10k_files"
temp=os.path.join(filepath,"temp.txt")
temp1=os.path.join(filepath,"newfile.txt")
LOG=os.path.join(filepath,"DOWNLOADLOG.txt")
with open(LOG,'w') as f:
    f.write("Filer\tSECTIONS\n")
    f.close()
txt_files = glob.glob(os.path.join(filepath, "*.txt"))
for Filer in txt_files:
        FileNUM = os.path.basename(Filer).split('.')[0]
        print("processing:",FileNUM )

        with open(LOG, 'a') as log:
            log.write(f"Processing: {FileNUM}\n")
        parse(Filer, temp)
        headerclean(temp, temp1)
        with open(temp,'r') as f:
            str1=f.read()
            output=str1
            locations_xbrlbig=xbrl_clean("<type>zip", "</document>", output)
            locations_xbrlbig.append(len(output))
            if locations_xbrlbig!=[]:
                str1=""
                if len(locations_xbrlbig)%2==0:
                    for i in range(0,len(locations_xbrlbig),2):
                        str1=str1+output[locations_xbrlbig[i]:locations_xbrlbig[i+1]]
        f.close
        output=str1

        # before cleaning:
        # test=str1.lower()
        # print("before cleaning:")
        # keywords = ["item 1", "item1", "item1a", "item 1a"]
        # for keyword in keywords:
        #     if keyword in test:
        #         print(f'Keyword "{keyword}" found in cleaned content.')
        #     else:
        #         print(f'Keyword "{keyword}" NOT found.')


        locations_xbrlbig=xbrl_clean("<type>graphic", "</document>", output)
        locations_xbrlbig.append(len(output))
        if locations_xbrlbig!=[0]:
            str1=""
            if len(locations_xbrlbig)%2==0:
                for i in range(0,len(locations_xbrlbig),2):
                    str1=str1+output[locations_xbrlbig[i]:locations_xbrlbig[i+1]]
        output=str1
        locations_xbrlbig=xbrl_clean("<type>excel", "</document>", output)
        locations_xbrlbig.append(len(output))
        if locations_xbrlbig!=[0]:
            str1=""
            if len(locations_xbrlbig)%2==0:
                for i in range(0,len(locations_xbrlbig),2):
                    str1=str1+output[locations_xbrlbig[i]:locations_xbrlbig[i+1]]      
        output=str1
        locations_xbrlbig=xbrl_clean("<type>pdf", "</document>", output)
        locations_xbrlbig.append(len(output))
        if locations_xbrlbig!=[0]:
            str1=""
            if len(locations_xbrlbig)%2==0:
                for i in range(0,len(locations_xbrlbig),2):
                    str1=str1+output[locations_xbrlbig[i]:locations_xbrlbig[i+1]]
        output=str1
        locations_xbrlbig=xbrl_clean("<type>xml", "</document>", output)
        locations_xbrlbig.append(len(output))
        if locations_xbrlbig!=[0]:
            str1=""
            if len(locations_xbrlbig)%2==0:
                for i in range(0,len(locations_xbrlbig),2):
                    str1=str1+output[locations_xbrlbig[i]:locations_xbrlbig[i+1]]
        output=str1
        locations_xbrlbig=xbrl_clean("<type>ex", "</document>", output)
        locations_xbrlbig.append(len(output))
        if locations_xbrlbig!=[0]:
            str1=""
            if len(locations_xbrlbig)%2==0:
                for i in range(0,len(locations_xbrlbig),2):
                    str1=str1+output[locations_xbrlbig[i]:locations_xbrlbig[i+1]]
        p = re.compile(r'(<DIV.*?>)|(<DIV\n.*?>)|(<DIV\n\r.*?>)|(<DIV\r\n.*?>)|(<DIV.*?\n.*?>)|(<DIV.*?\n\r.*?>)|(<DIV.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<div.*?>)|(<div\n.*?>)|(<div\n\r.*?>)|(<div\r\n.*?>)|(<div.*?\n.*?>)|(<div.*?\n\r.*?>)|(<div.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<TD.*?>)|(<TD\n.*?>)|(<TD\n\r.*?>)|(<TD\r\n.*?>)|(<TD.*?\n.*?>)|(<TD.*?\n\r.*?>)|(<TD.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<td.*?>)|(<td\n.*?>)|(<td\n\r.*?>)|(<td\r\n.*?>)|(<td.*?\n.*?>)|(<td.*?\n\r.*?>)|(<td.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<TR.*?>)|(<TR\n.*?>)|(<TR\n\r.*?>)|(<TR\r\n.*?>)|(<TR.*?\n.*?>)|(<TR.*?\n\r.*?>)|(<TR.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<tr.*?>)|(<tr\n.*?>)|(<tr\n\r.*?>)|(<tr\r\n.*?>)|(<tr.*?\n.*?>)|(<tr.*?\n\r.*?>)|(<tr.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<FONT.*?>)|(<FONT\n.*?>)|(<FONT\n\r.*?>)|(<FONT\r\n.*?>)|(<FONT.*?\n.*?>)|(<FONT.*?\n\r.*?>)|(<FONT.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<font.*?>)|(<font\n.*?>)|(<font\n\r.*?>)|(<font\r\n.*?>)|(<font.*?\n.*?>)|(<font.*?\n\r.*?>)|(<font.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<P.*?>)|(<P\n.*?>)|(<P\n\r.*?>)|(<P\r\n.*?>)|(<P.*?\n.*?>)|(<P.*?\n\r.*?>)|(<P.*?\r\n.*?>)')
        str1=p.sub("",str1)
        p = re.compile(r'(<p.*?>)|(<p\n.*?>)|(<p\n\r.*?>)|(<p\r\n.*?>)|(<p.*?\n.*?>)|(<p.*?\n\r.*?>)|(<p.*?\r\n.*?>)')
        str1=p.sub("",str1)
        str1=str1.replace("</DIV>","")
        str1=str1.replace("</div>","")
        str1=str1.replace("</TR>","")
        str1=str1.replace("</tr>","")
        str1=str1.replace("</TD>","")
        str1=str1.replace("</td>","")
        str1=str1.replace("</FONT>","")
        str1=str1.replace("</font>","")
        str1=str1.replace("</P>","")
        str1=str1.replace("</p>","")
        output=str1



# after here

        # locations_xbrlsmall=xbrl_clean("<xbrl", "</xbrl.*>", output)
        # locations_xbrlsmall.append(len(output))
        # if locations_xbrlsmall!=[0]:
        #     str1=""
        #     if len(locations_xbrlsmall)%2==0:
        #         for i in range(0,len(locations_xbrlsmall),2):
        #             str1=str1+output[locations_xbrlsmall[i]:locations_xbrlsmall[i+1]]
       
        # output1=table_clean('<table','</table>',str1)
        # str1=table_clean('<table','</table>',str1)
        str1=str1.replace("\r\n"," ")
        p = re.compile(r'<.*?>')
        str1=p.sub("",str1)



# before here



        str1=str1.replace("&nbsp;"," ")
        str1=str1.replace("&NBSP;"," ")
        str1=str1.replace("&LT;","LT")
        str1=str1.replace("&#60;","LT")
        str1=str1.replace("&#160;"," ")
        str1=str1.replace("&AMP;","&")
        str1=str1.replace("&amp;","&")
        str1=str1.replace("&#38;","&")
        str1=str1.replace("&APOS;","'")
        str1=str1.replace("&apos;","'")
        str1=str1.replace("&#39;","'")
        str1=str1.replace('&QUOT;','"')
        str1=str1.replace('&quot;','"')
        str1=str1.replace('&#34;','"')
        str1=str1.replace("\t"," ")
        str1=str1.replace("\v","")
        str1=str1.replace("&#149;"," ")
        str1=str1.replace("&#224;","")
        str1=str1.replace("&#145;","")
        str1=str1.replace("&#146;","")
        str1=str1.replace("&#147;","")
        str1=str1.replace("&#148;","")
        str1=str1.replace("&#151;"," ")
        str1=str1.replace("&#153;","") 
        str1=str1.replace("&#111;","")
        str1=str1.replace("&#153;","")
        str1=str1.replace("&#253;","")
        str1=str1.replace("&#8217;","")
        str1=str1.replace("&#32;"," ")
        str1=str1.replace("&#174;","")
        str1=str1.replace("&#167;","")
        str1=str1.replace("&#169;","")
        str1=str1.replace("&#8220;","")
        str1=str1.replace("&#8221;","")
        str1=str1.replace("&rsquo;","")
        str1=str1.replace("&lsquo;","")
        str1=str1.replace("&sbquo;","")
        str1=str1.replace("&bdquo;","")
        str1=str1.replace("&ldquo;","")
        str1=str1.replace("&rdquo;","")
        str1=str1.replace("\'","")
        p = re.compile(r'&#\d{1,5};')
        str1=p.sub("",str1)
        p = re.compile(r'&#.{1,5};')
        str1=p.sub("",str1)
        str1=str1.replace("_"," ")
        str1=str1.replace("and/or","and or")
        str1=str1.replace("-\n"," ")
        p = re.compile(r'\s*-\s*')
        str1=p.sub(" ",str1)
        p = re.compile(r'(-|=)\s*')
        str1=p.sub(" ",str1)
        p = re.compile(r'\s\s*')
        str1=p.sub(" ",str1)
        p = re.compile(r'(\n\s*){3,}')
        str1=p.sub("\n\n",str1)
        p = re.compile(r'<.*?>')
        str1=p.sub("",str1)

# # after:
#         test=str1.lower()
#         print("after cleaning:")
#         keywords = ["items 1 and 2. business and properties", "item 1a. risk factors"]
#         for keyword in keywords:
#             if keyword in test:
#                 print(f'Keyword "{keyword}" found in cleaned content.')
#             else:
#                 print(f'Keyword "{keyword}" NOT found.')



        item1={}
        item1[1] = "item 1: business"
        item1[2] = "item1: business"
        item1[3] = "item 1:business"
        item1[4] = "item1:business"
        item1[5] = "item 1 : business"
        item1[6] = "item1 : business"
        item1[7] = "item1: business"
        item1[8] = "item 1. business"
        item1[9] = "item1. business"
        item1[10] = "item 1.business"
        item1[11] = "item1.business"
        item1[12] = "item 1 . business"
        item1[13] = "item1 . business"
        item1[14] ="items 1 and 2. business and properties"
        item1[15]="item 1. businessoverview"
        item1[16]="item 1.businessgeneral"

        item1a={}
        item1a[1] = "item 1a: risk factors"
        item1a[2] = "item1a: risk factors"
        item1a[3] = "item 1a:risk factors"
        item1a[4] = "item1a:risk factors"
        item1a[5] = "item 1a : risk factors"
        item1a[6] = "item1a : risk factors"
        item1a[7] = "item 1a: risk factors"
        item1a[8] = "item1a: risk factors"
        item1a[9] = "item 1a. risk factors"
        item1a[10] = "item1a. risk factors"
        item1a[11] = "item 1a.risk factors"
        item1a[12] = "item1a.risk factors"
        item1a[13] = "item 1a . risk factors"
        item1a[14] = "item1a . risk factors"
        item1a[15] = "item1a. risk factors"

        look={"see ", " refer to ", " included in "," contained in ","in conjunction with","as discussed in"}
        a={}
        c={}
        lstr1=str1.lower()


# test
        with open("afterclean", 'w') as f:
                        f.write(lstr1)
                        f.close()


        for j in range(1,17):
            a[j]=[]
            for m in re.finditer(item1[j], lstr1):
                if not m:
                    break 
                substr1=lstr1[max(0,m.start()-50):m.start()]
                if any(s in substr1 for s in look):   
                    continue
                b=m.start()
                a[j].append(b)
        # print(a)
        list1=[]
        for value in a.values():
            for thing1 in value:
                list1.append(thing1)
        list1.sort()
        list1.append(len(lstr1))
        # print(list1)
        for j in range(1,16):
            c[j]=[]
            for m in re.finditer(item1a[j], lstr1):
                if not m:
                    break
                substr1=lstr1[max(0,m.start()-50):m.start()]
                after = lstr1[m.start():m.start() + 100].strip()
                # if any(s in substr1 for s in look) or not re.match(r'\s*item\s+1\b', after, re.IGNORECASE):
                if any(s in substr1 for s in look):

                    continue
                if re.match(r'[^\w]*item\s*1a[.:]?', after, re.IGNORECASE):

                    b=m.start()
                    c[j].append(b)
        # print(c)
        list2=[]
        for value in c.values():
            for thing2 in value:
                list2.append(thing2)
        list2.sort()
        locations={}
        if list2==[]:
            print("NOT FOUND")
        else:
            if list1==[]:
                print("NOT FOUND")
            else:
                for k0 in range(len(list1)):
                    locations[k0]=[]
                    locations[k0].append(list1[k0])
                for k0 in range(len(locations)):
                    for item in range(len(list2)):
                        if locations[k0][0]<=list2[item]:
                            after = lstr1[list2[item]:list2[item] + 100].strip()
                            if len(locations[k0]) == 1 or re.match(r'[^\w]*item\s*1a[.:]?', after, re.IGNORECASE):
                                locations[k0].append(list2[item])
                                break
                    if len(locations[k0])==1:
                        del locations[k0]
        original_file_name = os.path.basename(FileNUM)  
        extracted_file_name = f"extracted {original_file_name}"     
        if locations=={}:
            with open(LOG,'a') as f:
                f.write(str(FileNUM)+"\t"+"0\n")
                f.close()
        else:
            sections=0
            substring2=""
            for k0 in range(len(locations)): 
                substring2=str1[locations[k0][0]:locations[k0][1]]
                substring3=substring2.split()
                if len(substring3)>250:
                    sections=sections+1
                    with open(extracted_file_name, 'w') as f:
                        f.write("<SECTION>\n")
                        f.write(substring2+"\n")
                        f.write("</SECTION>\n")
                        f.close()
            with open(LOG,'a') as f:
                    f.write(str(FileNUM)+"\t"+str(sections)+"\n")
                    f.close()
        # print(FileNUM)

