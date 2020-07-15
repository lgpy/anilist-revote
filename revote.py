import media
import eel
import argparse

parser = argparse.ArgumentParser(description='Arguments:')
parser.add_argument('-t', action="store", dest="type",default="anime",help='defines type (Anime,Manga)')
parser.add_argument('-f', action="store", dest="format",help='defines format for anime (TV,TV Short,OVA,Special,Movie,ONA,Music)')

args = parser.parse_args()

list=media.getlist(args.type.upper(),args.format)
if list!=None:
    count = -1
    eel.init('web')


    @eel.expose
    def previous():
        global count
        if count>0:
            count-=1
            tempinfo = list[count]
        else:
            tempinfo = list[count]
            eel.sendalert('There is nothing there...')
        return {"Count": count+1,"Total": len(list),"Title": tempinfo['media']['title']['romaji'], "Image": tempinfo['media']['coverImage']['large'],
                "Score": tempinfo['score'], 'MeanScore': tempinfo['media']['averageScore']}

    @eel.expose
    def next():
        global count
        if count+1 < len(list):
            count += 1
            tempinfo = list[count]
        else:
            tempinfo = list[count]
            eel.sendalert('There is nothing there...')
        return {"Count": count+1,"Total": len(list),"Title": tempinfo['media']['title']['romaji'], "Image": tempinfo['media']['coverImage']['large'],
                "Score": tempinfo['score'], 'MeanScore': tempinfo['media']['averageScore']}

    @eel.expose
    def save(score):
        print("Changed score of " + list[count]['media']['title']['romaji'] + " from " + str(list[count]['score']) + " to " + score)
        score=int(score)
        list[count]['score']=score
        media.changeScore(score, list[count]['media']['id'])
        return 1;

    eel.start('index.html',size=(816,539))






