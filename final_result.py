audio_hit_file = "one.txt"
audio_miss_file = "two.txt"
image_out_file = "three.txt"

threshold = 0.5

# results = jednotlive log. pravdepodobnosti jednotlivych testu
def Calculate(results):
    return sum(results)/len(results)

def main():
    res = {}
    
    with open(audio_hit_file, 'r') as f: audio_hits = f.readlines()

    for line in audio_hits:
        content = line.split(' ')
        if not content[0] in res.keys(): res[content[0]] = {}
        res[content[0]]['audio_hit'] = content[1]

    with open(image_out_file, 'r') as f: image_out = f.readlines()

    for line in image_out:
        content = line.split(' ')
        if not content[0] in res.keys(): res[content[0]] = {}
        res[content[0]]['image_out'] = content[1]

    for f in res:
        result = res[f]
        if 'audio_hit' in result.keys() and 'image_out' in result.keys():
            score = Calculate([float(result['audio_hit']), float(result['image_out'])])
            if score > threshold: decision = 1
            else: decision = 0 
            print("{} {} {}".format(f, round(score*10000)/10000, decision))


main()