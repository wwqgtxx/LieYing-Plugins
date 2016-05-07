
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

def makeFormatLabel( f ):
    label = f.get('format','')
    if len(label) > 0 :
        return label
    label = f.get('format_note','')
    if len(label) == 0:
        label = str(f.get('format_id',''))
    resolution = str(f.get('resolution', ''))
    if len(resolution) == 0:
        width = str(f.get('width',''))
        height = str(f.get('height',''))
        if len(width) > 0 and len(height) > 0:
            resolution = '%sx%s' % (width,height)
    if len(resolution) > 0:
        label = label + '_' + resolution
    vcodec = f.get('vcodec','')
    acodec = f.get('acodec','')
    if len(vcodec) > 0 or len(acodec) > 0:
        if len(acodec) == 0 or acodec == "none":
            label = label + '(video_only)'
        elif len(vcodec) == 0 or vcodec == "none":
            label = label + '(audio_only)'
    return label

def convertVideo( info, proxy = None ):
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
                'urls' : info.get('url',''),
                'proxy' : proxy
                }]            
            })
    else:
        for f in formats:
            ext = f.get('ext','')
            url = f.get('url','')
            if url[0:5] != 'http:' and url[0:6] != 'https:':
                continue
            data.append({
                'label' : '单段_%s_%s' %  (makeFormatLabel(f), ext.upper() ),
                'size' : formatSize( f.get('filesize',0) ),
                'download' : [{
                    'protocol' : f.get('protocol', url[:url.find(':')]),
                    'urls' : [ url ],
                    'duration' : f.get('duration',''),
                    'args' : f.get('http_headers',''),
                    'proxy' : proxy,
                    'length' : f.get('filesize',0)
                    }]
                }) 
    assert len(data) != 0, ' youtube-dl 暂时无法支持指定网址'
    result['data'] = data
    return result

def convertMultiVideo( info, proxy = None ):
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
                    url = entryF.get('url','')
                    if url[0:5] != 'http:' and url[0:6] != 'https:':
                        continue
                    download.append({
                        'protocol' : entryF.get('protocol','http'),
                        'urls' : [entryF.get('url','')],
                        'duration' : entry.get('duration',''),
                        'args' : entryF.get('http_headers', ''),
                        'proxy' : proxy,
                        'length' : entryF.get('filesize',0)
                    })
                    size =  size + int(entryF.get('filesize',0))
                    break
        if len(download) == 0:
            continue
        ext = f.get('ext','')
        one = {
            'label': '多段_%s_%s' % ( f.get('format','') or code, ext.upper()),
            'ext': ext,
            'size' : formatSize(size),
            'download' : download
            }
        data.append(one)
    assert len(data) != 0, ' youtube-dl 暂时无法支持指定网址'
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
    p = None
    if 'downProxy' in info:
        p = info.get('downProxy')
    if t == "multi_video":
        return convertMultiVideo(info, p)
    elif t == "video":
        return convertVideo(info, p)
    elif t == "playlist":
        return convertPlaylist(info)

    return info
