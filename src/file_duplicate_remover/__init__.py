import os

parentPath = "C:\\Users\\Apollo\\Music"
musicFormats = ['wma','MP3', 'mp3','m4a','wav']

nRemovedFiles = 0
removedMBs = 0

def getMBs(path):
    return os.path.getsize(path=path)/10e6

def searchEquivalent(comparisonLink, link):
    # if os.path.isfile(link) and link[-3:] in musicFormats:
    #     if comparisonLink!=link and comparisonLink[comparisonLink.rfind('\\')+1:-4] == link[link.rfind('\\')+1:-4]:
    #         removedMBs += getMBs(path=path)
    #         os.remove(path=link)
    #         nRemovedFiles += 1
    #         print(f"removed {link} due to {comparisonLink}")
    #     return
    for file in os.listdir(link):
        jointLink = os.path.join(link,file)
        if os.path.isdir(jointLink):
            # deleting empty directories                            
            if not os.listdir(jointLink):
                os.remove(jointLink)
            else:
                searchEquivalent(comparisonLink,jointLink)
        if os.path.isfile(jointLink) and jointLink[-3:] in musicFormats:
            if comparisonLink != jointLink and comparisonLink[comparisonLink.rfind('\\') + 1:-4] == jointLink[jointLink.rfind('\\') + 1:-4]:
                removedMBs += getMBs(jointLink)
                os.remove(path=jointLink)
                nRemovedFiles += 1
                print(f"removed {jointLink} due to {comparisonLink}")


def digTilFile(link):
    # if os.path.isfile(link) and link[-3:] in musicFormats:
    #     print(f"searching for equivalent for {link}...")
    #     searchEquivalent(link,parentPath)
    #     return
    for file in os.listdir(link):
        jointLink = os.path.join(link,file)
        if os.path.isdir(jointLink):
            digTilFile(jointLink)
        if os.path.isfile(jointLink) and jointLink[-3:] in musicFormats:
            print(f"searching equivalent for {jointLink}...")
            searchEquivalent(jointLink,parentPath)

if __name__ == '__main__':
    digTilFile(parentPath)
    print(f"removed {nRemovedFiles} files of {removedFileSize} MBs of accumulated size")