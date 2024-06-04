import subprocess
import os

#davis
name_list = ['bear', 'blackswan', 'bmx-bumps', 'bmx-trees', 
             'boat', 'breakdance', 'breakdance-flare', 'bus', 
             'camel', 'car-roundabout', 'car-shadow', 'car-turn', 'cows', 
             'dance-jump', 'dance-twirl', 'dog', 'dog-agility', 
             'drift-chicane', 'drift-straight', 'drift-turn', 
             'elephant', 'flamingo', 'goat', 'hike', 'hockey', 
             'horsejump-high', 'horsejump-low', 'kite-surf', 'kite-walk', 
             'libby', 'lucia', 'mallard-fly', 'mallard-water', 'motocross-bumps', 
             'motocross-jump', 'motorbike', 'paragliding', 'paragliding-launch', 
             'parkour', 'rhino', 'rollerblade', 'scooter-black', 'scooter-gray', 
             'soapbox', 'soccerball', 'stroller', 'surf', 'swing', 'tennis', 'train']

epoch = 300
model_size_list = [0.5, 1.0, 1.5, 2.0]
size_n = 128
lr = 0.00099
#lr = 0.001

for name in name_list:
    outf = f'davis_{name}'
    img_path = f'dataset/DAVIS-data/DAVIS/JPEGImages/1080p/{name}'
    for i in range(len(model_size_list)):
        model_size = model_size_list[i]
        print(name, img_path)
        #porposed
        subprocess.run(f'python train_nerv_all.py -e {epoch} --data_path {img_path} --lr {lr} --exp_id {name}_{str(model_size)} --outf {outf} --modelsize {model_size} --size_n {size_n} --use_rchnerv', shell=True)
        eval_path = f'output/{outf}/{name}_{str(model_size)}/model_latest.pth'
        subprocess.run(f'python train_nerv_all.py -e {epoch} --data_path {img_path} --lr {lr} --exp_id {name}_{str(model_size)}_eval --outf {outf} --modelsize {model_size} --size_n {size_n} --use_rchnerv --eval_only --weight {eval_path} --dump_images --dump_videos', shell=True)
        #HNeRV
        subprocess.run(f'python train_nerv_all.py -e {epoch} --data_path {img_path} --lr {lr} --exp_id {name}_{str(model_size)}_hnerv --outf {outf} --modelsize {model_size}', shell=True)
        hnerv_eval_path = f'output/{outf}/{name}_{str(model_size)}_hnerv/model_latest.pth'
        subprocess.run(f'python train_nerv_all.py -e {epoch} --data_path {img_path} --lr {lr} --exp_id {name}_{str(model_size)}_hnerv_eval --outf {outf} --modelsize {model_size} --eval_only --weight {hnerv_eval_path} --dump_images --dump_videos', shell=True)
        #val.py
        pro_path = f'output/{outf}/{name}_{str(model_size)}_eval'
        hnerv_path = f'output/{outf}/{name}_{str(model_size)}_hnerv_eval'
        subprocess.run(f'python val.py --pro_path {pro_path} --hnerv_path {hnerv_path}', shell=True)
        subprocess.run(f'python compare.py --pro_path {pro_path} --hnerv_path {hnerv_path}', shell=True)
subprocess.run(f'python excel.py --path output', shell=True)
