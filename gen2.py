from itertools import combinations

'''
Author: Ethan Roland
Date: 4/30/19
Produces all possible string mixes
'''

def mix(str1, str2):

    print('---')

    #generates EditDist array
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j    # Min. operations = j
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],      # Insert
                                   dp[i-1][j],      # Remove
                                   dp[i-1][j-1])    # Replace

    '''
    #prints ED array
    print('',end='\t\t')
    for let in str2:
        print(let,end='\t')
    print()
    for i in range(m+1):
        if i > 0:
            print(str1[i-1],end='\t')
        else:
            print('',end='\t')
        for j in range(n+1):
            print(dp[i][j],end='\t')
        print()
    print('---')
    '''

    print('rank is\t\t\t\t\t',dp[m][n])

    #gives paths from s1->s2
    paths = []
    path = []
    gen(paths,path,' '+str1,' '+str2,dp,m,n,str2)

    #gives all combinations of paths with len = lim
    lim = (int)(dp[m][n]/2)
    moves = set()
    for el in paths:
        #print(el)
        comb = combinations(el,lim)
        for c in comb:
            #print(c)
            moves.add(c)
    #print(len(moves))

    #executes calculated moves
    out = set()
    for el in moves:
        #print(el)
        word = str2
        temp = []
        for m in el:
            if '+' not in m[1]:
                word = word[:m[0]] + m[1] + word[m[0]+1:]
            else:
                temp.append(m)
        d = 0
        for m in temp:
            #print(word,m)
            word = word[:m[0]+d] + m[1][1] + word[m[0]+d:]
            d += 1
        word = word.replace('-','')
        out.add(word)

    print('mixed words, lm =',lim,'\t',len(out))
    out2 = set()

    #determines if gen'd word is acceptable
    for el in out:
        if proper(el,str1,str2):
            out2.add(el)

    print('accepted words \t\t\t',len(out2))
    print('---')

    return out2

def gen(paths,path,s1,s2,arr,x,y,word):

    #print('----',x,y,word)

    if arr[x][y] == 0:
        #print('RETURN')
        #print(path)
        paths.append(path)
        return

    cur = arr[x][y]
    try:
        lf = arr[x][y-1]
    except:
        lf = 1000
    try:
        up = arr[x-1][y]
    except:
        up = 1000
    try:
        di = arr[x-1][y-1]
    except:
        di = 1000

    #if letters are the same
    if s1[x] == s2[y]:
        #print('same')
        gen(paths,path,s1,s2,arr,x-1,y-1,word)
        return

    #finds all minimum next steps
    next = {(x,y-1):lf}
    if up == lf:
        next[(x-1,y)] = up
    elif up < lf:
        next.clear()
        next[(x-1,y)] = up
    if di == min(lf,up):
        next[(x-1,y-1)] = di
    elif di < min(lf,up):
        next.clear()
        next[(x-1,y-1)] = di

    #for m in next.keys():
    #   print(m)

    #performs edits
    for m in next.keys():
        #print(x,y,'-->',m[0],m[1])
        if m[0] == x-1 and m[1] == y-1: #diagonal/replace
            temp = word[:y-1] + s1[x] + word[y:]
            p2 = path.copy()
            p2.append((y-1,s1[x]))
            #print('di/replace',temp)
            gen(paths,p2,s1,s2,arr,x-1,y-1,temp)
        if m[0] == x-1 and m[1] == y: #up/insert
            temp = word[:y] + s1[x] + word[y:]
            p2 = path.copy()
            p2.append((y,'+'+s1[x]))
            #print('up/insert',temp)
            gen(paths,p2,s1,s2,arr,x-1,y,temp)
        if m[0] == x and m[1] == y-1: #left/delete
            temp = word[:y-1] + word[y:]
            p2 = path.copy()
            p2.append((y-1,'-'))
            #print('left/delete',temp)
            gen(paths,p2,s1,s2,arr,x,y-1,temp)
    return

def proper(input,s1,s2) :
    if input[0] != s1[0] and input[0] != s2[0]:
        return False
    #return True
    v = 0
    c = 0
    for let in input:
        if let in 'aeiou':
            c = 0
            v += 1
        else: #is a consonant
            v = 0
            c += 1
        if c > 2 or v > 1:
            return False
    return True
