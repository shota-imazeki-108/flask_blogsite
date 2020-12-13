import flaskblog.girls.stylegan2
import pretrained_networks
import dnnlib
import dnnlib.tflib as tflib
from google_drive_downloader import GoogleDriveDownloader as gdd
import numpy as np
import PIL.Image
from tqdm import tqdm
from math import ceil
import time


class GirlsGenerator:
    def __init__(self):
        url = 'https://drive.google.com/open?id=1WNQELgHnaqMTq3TlrnDaVkyrAH8Zrjez'
        model_id = url.replace('https://drive.google.com/open?id=', '')

        # path変える必要あり: os.path.dirname(__file__)
        network_pkl = '/content/models/model_%s.pkl' % model_id
        gdd.download_file_from_google_drive(
            file_id=model_id, dest_path=network_pkl)
        _G, _D, Gs = pretrained_networks.load_networks(network_pkl)
        self.__Gs = Gs

    def generate(self, size=9, psi=0.5):
        try:
            # generate 9 random seeds
            self.utc = time.time()
            seeds = np.random.randint(10000000, size=size)
            print(seeds)

            zs = self.generate_zs_from_seeds(seeds)
            imgs = self.generate_images(zs, psi)
            img = self.createImageGrid(imgs)
            img = img.convert("RGB")
            img.save(f'girls_{self.utc}.jpg', quality=95)
            return self.utc
        except Exception:
            print('Failed!')

    def generate_zs_from_seeds(self, seeds):
        zs = []
        for seed_idx, seed in enumerate(seeds):
            rnd = np.random.RandomState(seed)
            # [minibatch, component]
            z = rnd.randn(1, *self.__Gs.input_shape[1:])
            zs.append(z)
        return zs

    # Trunctation psi value needed for the truncation trick
    def generate_images(self, zs, truncation_psi):
        # Get tf noise variables, for the stochastic variation
        noise_vars = [
            var for name,
            var in self.__Gs.components.synthesis.vars.items() if name.startswith('noise')]

        Gs_kwargs = dnnlib.EasyDict()
        Gs_kwargs.output_transform = dict(
            func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        Gs_kwargs.randomize_noise = False
        if not isinstance(truncation_psi, list):
            truncation_psi = [truncation_psi] * len(zs)

        imgs = []
        for z_idx, z in tqdm(enumerate(zs)):
            Gs_kwargs.truncation_psi = truncation_psi[z_idx]
            noise_rnd = np.random.RandomState(1)  # fix noise
            tflib.set_vars({var: noise_rnd.randn(*var.shape.as_list())
                            for var in noise_vars})  # [height, width]
            # [minibatch, height, width, channel]
            images = self.__Gs.run(z, None, **Gs_kwargs)
            imgs.append(PIL.Image.fromarray(images[0], 'RGB'))

        # Return array of PIL.Image
        return imgs

    def generate_images_from_seeds(self, seeds, truncation_psi):
        return self.generate_images(
            self.generate_zs_from_seeds(seeds),
            truncation_psi)

    def createImageGrid(self, images, scale=0.25, rows=1):
        w, h = images[0].size
        w = int(w * scale)
        h = int(h * scale)
        height = rows * h
        cols = ceil(len(images) / rows)
        width = cols * w
        canvas = PIL.Image.new('RGBA', (width, height), 'white')
        for i, img in enumerate(images):
            img = img.resize((w, h), PIL.Image.ANTIALIAS)
            canvas.paste(img, (w * (i % cols), h * (i // cols)))
        return canvas
