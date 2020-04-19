"""
parse MSCOCO annotation
"""

from pycocotools.coco import COCO

def _pp(l): # pretty printing 
    for i in l: print('{}: {}'.format(i,l[i]))

def parse_mscoco_annot(ANN, pick, exclusive = False):
    print('Parsing for {} {}'.format(
            pick, 'exclusively' * int(exclusive)))

    dumps = list()
    # initialize COCO api for instance annotations
    coco = COCO(ANN)

    img_ids = coco.getImgIds()

    for img in coco.loadImgs(img_ids):
        anns = list()
        for ann in coco.loadAnns(coco.getAnnIds(img['id'])):
            cat = coco.loadCats(ann['category_id'])[0]
            if cat['name'] not in pick: 
                continue
            bbox = ann['bbox']
            anns += [[cat['name'], bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]]
        dumps += [[img['file_name'], [img['width'], img['height'], anns]]]

    # gather all stats
    stat = dict()
    for dump in dumps:
        all = dump[1][2]
        for current in all:
            if current[0] in pick:
                if current[0] in stat:
                    stat[current[0]]+=1
                else:
                    stat[current[0]] =1

    print('\nStatistics:')
    _pp(stat)
    print('Dataset size: {}'.format(len(dumps)))

    return dumps
