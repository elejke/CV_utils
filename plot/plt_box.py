import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
# show plt_img in front
from io import BytesIO
import base64

num_class = 100

# use cmap color | tab20, tab20b, hsv
cmap = plt.get_cmap('hsv')  # qualitative cmaps, >18
cNorm = mcolors.Normalize(vmin=0, vmax=num_class - 1)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)


def show_colors():
    for idx in range(num_class):
        print(scalarMap.to_rgba(idx))


show_colors()


def plt_bbox(img, boxes, labels, class2names, send_web=True):
    plt.figure(figsize=(6, 4))
    # plt.xticks([])
    # plt.yticks([])
    plt.axis('off')
    plt.imshow(img)

    for label_id, box in zip(labels, boxes):
        # label_id = names2class[label]
        label_id -= 1  # detect idx
        # box
        plt.gca().add_patch(plt.Rectangle(xy=(box[0], box[1]),
                                          width=box[2] - box[0],
                                          height=box[3] - box[1],
                                          edgecolor=scalarMap.to_rgba(label_id),  # get color from label_id
                                          fill=False, linewidth=2))
        # name
        plt.annotate(class2names[label_id],
                     xy=(box[0], box[1]), fontsize=10,
                     xycoords='data', xytext=(2, 5), textcoords='offset points',
                     bbox=dict(boxstyle='round, pad=0.3',  # linewidth=0 可以不显示边框
                               facecolor=scalarMap.to_rgba(label_id), lw=0),
                     color='w')

    if send_web:
        # save for front img result
        sio = BytesIO()
        plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
        data = base64.encodebytes(sio.getvalue()).decode()
        img_src = 'data:image/png;base64,{}'.format(data)
        return img_src
    else:
        plt.show()
