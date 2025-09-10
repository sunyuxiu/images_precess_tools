import argparse
import os
import cv2
from time import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


class VideoFrameExtractor:
    def __init__(self, root_path, out_path, skip_frame=5, jpg_quality=80, workers=8):
        self.root_path = root_path
        self.out_path = out_path
        self.skip_frame = skip_frame
        self.jpg_quality = jpg_quality
        self.workers = workers

        assert os.path.exists(self.root_path), "root_path does not exist"
        os.makedirs(self.out_path, exist_ok=True)

        self.video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')

    def v2i(self, src, out_path):
        """将视频转换为图片，全部存入统一目录，文件名用时间戳"""
        vc = cv2.VideoCapture(src)
        num = 0
        saved = 0
        start_time = int(time() * 1000)

        if vc.isOpened():
            rval, frame = vc.read()
            while rval:
                if num % self.skip_frame == 0:
                    filename = f"{start_time}_{saved}.jpg"
                    path = os.path.join(out_path, filename)
                    cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpg_quality])
                    saved += 1
                rval, frame = vc.read()
                num += 1
        vc.release()

    def filter_video(self):
        """多线程处理所有视频"""
        video_tasks = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            for name in os.listdir(self.root_path):
                src = os.path.join(self.root_path, name)
                if os.path.isfile(src) and name.lower().endswith(self.video_extensions):
                    video_tasks.append(executor.submit(self.v2i, src, self.out_path))

            for future in tqdm(as_completed(video_tasks), total=len(video_tasks), desc="Processing Videos"):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing a video: {e}")


def parse_opt():
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument('root_path', help='Input video folder path')
    parser.add_argument('out_path', help='Output image folder path')
    parser.add_argument('--skip', type=int, default=25, help='Skip every N frames')
    parser.add_argument('--jpg_quality', type=int, default=80, help='JPG quality')
    parser.add_argument('--workers', type=int, default=60, help='Number of worker threads')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_opt()
    extractor = VideoFrameExtractor(args.root_path, args.out_path, args.skip, args.jpg_quality, args.workers)
    extractor.filter_video()
