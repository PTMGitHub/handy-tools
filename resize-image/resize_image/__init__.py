import logging
import os
from PIL import Image
from art import *


class ResizeImage:
    def __init__(self) -> None:
        self.setup_logger()
        self.images_in_file_path = os.environ.get(
            "IMAGES_IN_FILE_PATH", "resize_image/in"
        )


    def setup_logger(self) -> None:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
        )

    def start(self):
        logging.debug("Enter start()")
        logging.debug("Check in path exist")
        if os.path.exists(self.images_in_file_path):
            print("Getting list of images")
            returned_images_list = self.get_images_list()
            print("Image Size Reduction Started...")
            result = self.resize_images(returned_images_list)
            print("Image Size Reduction Done.")
            print(art("hug me"))
        else:
            logging.error(f"The following dir doesnt exist: {self.images_in_file_path}")
            print(art("sad and confused"))
            exit(1)

    def get_images_list(self) -> list:
        logging.debug("Enter get_images_list()")
        images_list = []
        logging.debug(f"Building list of images in dir:{self.images_in_file_path}")
        for path in os.listdir(self.images_in_file_path):
            if os.path.isfile(os.path.join(self.images_in_file_path, path)):
                images_list.append(path)
        logging.debug(f"images_list: {images_list}")
        logging.debug("Exit get_images_list()")
        return images_list

    def resize_images(self, images_list) -> list:
        for img in images_list:
            im = Image.open(self.images_in_file_path + "/" + img)
            width, height = im.size
            im = im.resize((width//2, height//2), Image.Resampling.LANCZOS)
            im.save(self.images_out_file_path + "/scaled/" + img)
            im.save(self.images_out_file_path + "/" + img, optimize=True, quality=70)


def main():
    resize_image = ResizeImage()
    resize_image.start()


if __name__ == "__main__":
    main()
