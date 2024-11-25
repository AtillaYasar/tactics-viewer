"""
USAGE
- put a tactics json in `dumpresponse.json`:
    + open dev tools -> https://tactics.dev/dashboard -> network tab -> find the `https://api.tactics.dev/getTactics?sort=%22mostRecentlyUsed%22` call -> response tab -> paste to file
- (optional) pip install colorama: https://pypi.org/project/colorama/

STRUCTURE
- general utils
- program-specific utils
- grab tactics from `dumpresponse.json`, or ask user to paste tactics into that file
- cli loop
"""

path = 'dumpresponse.json'

filterstring = "i['content'].strip()!=''"
filt = lambda i: eval(filterstring)
# removes empty tactics from display, it's a string because the cli displays the filter

import json, os


# general utils

def col(ft, s):
    """For printing text with colors.
    
    Uses ansi escape sequences. (ft is "first two", s is "string")"""
    # black-30, red-31, green-32, yellow-33, blue-34, magenta-35, cyan-36, white-37
    u = '\u001b'
    numbers = dict([(string,30+n) for n, string in enumerate(('bl','re','gr','ye','blu','ma','cy','wh'))])
    n = numbers[ft]
    return f'{u}[{n}m{s}{u}[0m'

def bgcol(ft, s):
    # same as col but 40 instead of 30 to get background
    u = '\u001b'
    numbers = dict([(string,40+n) for n, string in enumerate(('bl','re','gr','ye','blu','ma','cy','wh'))])
    n = numbers[ft]
    return f'{u}[{n}m{s}{u}[0m'

def writefile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2)
        else:
            f.write(content)

def readfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        if path.endswith('.json'):
            content = json.load(f)
        else:
            content = f.read()
    return content


# program-specific utils

def getsource(d):
    # tactic dict --> string
    edge = col('gr', f'--- source code, {len(d["content"].split("\n"))} lines ---')

    # add colors
    code = d['content']
    highlights = [ ('input', 'cy'), ('return', 'cy'), ('//', 'gr'), ('/*', 'gr'), ('*/', 'gr') ]
    for s, c in highlights:
        code = code.replace(s, col(c, s))

    lines = [ edge, code, edge ]
    return '\n'.join(lines)

def getpython(d):
    # tactic dict --> string
    code = """
y = { 'k1': 'var1', 'k2': 'var2' }
y = { 'input': y }
y = { 'initial_variables': y , 'tactic_id': 'idplaceholder' }
x = { 'Content-Type': 'application/json', 'X-API-KEY': tactics_key }
x = requests.post( 'https://api.tactics.dev/api/run' , headers=x, json=y)
print( x.json() )
    """[1:-1]
    code = code.replace('idplaceholder', d['id'])
    edge = col('gr', f'--- python api call ---')
    lines = [ edge, code, edge ]
    return '\n'.join(lines)

def getsubcall(d):
    # tactic dict --> string
    code = """
input = { "k1":"v1", "k2":"v2" };
ret = $tactic (`/nameplaceholder`, input) ;
return ret;
    """[1:-1]
    highlights = [ ('input', 'cy'), ('return', 'cy'), ('//', 'gr'), ('/*', 'gr'), ('*/', 'gr') ]
    for s, c in highlights:
        code = code.replace(s, col(c, s))
    code = code.replace( 'nameplaceholder', d['title'])

    edge = col('gr', f'--- subtactic call ---')
    lines = [ edge, code, edge ]
    return '\n'.join(lines)

def getcode(d):
    # tactic dict --> string
    return f'{getpython(d)}\n\n{getsubcall(d)}'

try:
    from colorama import init
    init()
except:
    col = lambda ft, s: s
    bgcol = lambda ft, s: s
    print('no `colorama` library found (https://pypi.org/project/colorama/), will print ugly')

try:
    tactics = readfile( path )['tactics']
    # list of dicts with: id, title, content, isPublic, owner
except Exception as e:
    print(e)
    print(col('re', f'couldnt find `tactics` key in `{path}` file'))
    exit()

col1 = lambda i: col('ma', i)
col2 = lambda i: col('blu', i)

# main loop to show tactics
    # inner loop to take input and validate it
while True:
    print(bgcol('cy', '-'*10))
    print( '[n]', col('cy', '[title]'), '[i] lines', col('ma', '\n  [first line]'), sep=col('ye', ' -- ') )
    print(bgcol('cy', '-'*10))
    [ print( n, col('cy', i['title']), f"{len(i['content'].split('\n'))} lines", col('ma', '\n  ' + i['content'].split('\n')[0] ) , sep=f' {bgcol("ye", "--")} ', flush=1 ) if filt(i) else None for n,i in enumerate(tactics) ]
    print( f'tactics filtered by: {col("ma", filterstring)}' )
    while True:
        print(bgcol('cy', '-'*10))
        inp = input(f'> type a {col1("number")} to get {col2("source code")} and {col2("code for calling this tactic")}, or {col1("s")} to see the {col2("tactics list")} again, or {col1('f = lambda i: "$do" in i["content"]')} to change the {col2('filter')}\n')
        if inp == 's':
            break
        else:
            parts = inp.split(' = ')
            if len(parts)==2:
                a, b = parts
                if a == 'f':
                    try:
                        filt = lambda i: eval(b)
                        filt(tactics[0])
                    except Exception as e:
                        print(e)
                        print(col('re', 'wrong input, reeeee'))
                        continue
                    else:
                        filterstring = b
                        filt = lambda i: eval(filterstring)
                        break
            else:
                try:
                    t = tactics[int(inp)]
                except Exception as e:
                    print(e)
                    print(col('re', 'wrong input, reeeee'))
                    continue
                else:
                    print(getsource(t))
                    print()
                    print(getcode(t))
                    print(col('cy', f'^^ n = {inp}, title = {t["title"]}'))
        print(bgcol('cy', '-'*10))
