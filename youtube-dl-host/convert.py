
def formatSize( size ) :
    if not size:
        return ''
    tail = "B"
    size = float(size)
    if size > 1024:
        size = size / 1024
        tail = "KB"
    if size > 1024:
        size = size / 1024
        tail = 'MB'
    if size > 1024:
        size = size /1024
        tail = 'GB'
    return '%.1f%s' % (size,tail)

def convertVideo( info ):
    result = {
        'type' : 'formats',
        'icon' : info.get('thumbnail',''),
        'name' : info.get('title','未知'),
        'provider' : info.get('extractor','')
        }
    formats = info.get('formats', [] )
    data = []
    if len(formats) == 0:
        data.append({
            'label' : info.get('format', '未知'),
            'ext' : info.get('ext', ''),
            'download' : [{
                'urls' : info.get('url','')
                }]            
            })
    else:
        for f in formats:
            ext = f.get('ext','')
            url = f.get('url','')
            data.append({
                'label' : '单段_%s_%s' %  (f.get('format','') or f.get('format_id','未知'), ext.upper() ),
                'size' : formatSize( f.get('filesize',0) ),
                'download' : [{
                    'protocol' : f.get('protocol', url[:url.find(':')]),
                    'urls' : [ url ],
                    'duration' : f.get('duration',''),
                    'args' : f.get('http_headers',''),
                    'length' : f.get('filesize',0)
                    }]
                }) 
    
    result['data'] = data
    return result

def convertMultiVideo( info ):
    result = {
        'type' : 'formats',
        'name' : info.get('title','未知'),
        'provider' : info.get('extractor','')
        }

    entries = info.get('entries',[])
    if len(entries) == 0:
        return None

    data = []
    formats = entries[0].get('formats',[])
    result['icon'] = entries[0].get('thumbnail','')
    for f in formats:
        code = f.get('format_id','未知')
        download = []
        size = 0
        for entry in entries:
            entryFormats = entry.get('formats',[])
            for entryF in entryFormats:
                if entryF.get('format_id','未知') == code:
                    download.append({
                        'protocol' : entryF.get('protocol','http'),
                        'urls' : [entryF.get('url','')],
                        'duration' : entry.get('duration',''),
                        'args' : entryF.get('http_headers', ''),
                        'length' : entryF.get('filesize',0)
                    })
                    size =  size + int(entryF.get('filesize',0))
                    break
        ext = f.get('ext','')
        one = {
            'label': '多段_%s_%s' % ( f.get('format','') or code, ext.upper()),
            'ext': ext,
            'size' : formatSize(size),
            'download' : download
            }
        data.append(one)
    result['data'] = data;
    return result

def convertPlaylist( info ):
    entries = info.get('entries', [])
    data = []
    index = 1
    for one in entries:
        data.append({
            'url' : one.get('url'),
            'no' : one.get('ie_key','') or str(index)
            })
        index = index + 1

    result = {
        'type' : 'list',
        'title' : info.get('title'),
        'data' : data
        }
    return result

def Convert( info ):
    t = info.get('_type', 'video')
    if t == "multi_video":
        return convertMultiVideo(info)
    elif t == "video":
        return convertVideo(info)
    elif t == "playlist":
        return convertPlaylist(info)

    return info
