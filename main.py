from wk_utils.config_manager import load_config
from wk_utils.log import init_logging
import threading
import traceback
import json
import uuid
import numpy as np
import cv2
import time
import os
import glob
from ultralytics import YOLO
import asyncio
import socket
import time


# class Detector:
#     def __init__(self):
#         self.DEV = True
#         # This is changed when ioss core got packets from entrypoint.
#         self.working_state = True

#         self.lg = init_logging('main')
#         self.lg.debug('loading model...')
#         self.model = YOLO('yolov8n.pt', task='detect', )
#         self.cf = load_config()

#         self.width = self.cf.getint('common', 'cap_width')
#         self.height = self.cf.getint('common', 'cap_height')

#         self.src = [np.ones((self.height, self.width, 3))]  # stream 저장되는 곳
#         self.cam_state = [0]  # 카메라 상태 저장되는 곳

#         t = threading.Thread(target=self._cam_thread, daemon=True, args=(
#             0, self.cf.getint('common', 'source'),))
#         t.start()

#     def _cam_thread(self, ns, source):
#         assert type(ns) == int
#         while True:
#             try:
#                 cap = cv2.VideoCapture(source)
#                 cap.set(cv2.CAP_PROP_FRAME_WIDTH,
#                         self.width)
#                 cap.set(cv2.CAP_PROP_FRAME_HEIGHT,
#                         self.height)
#                 cap.set(cv2.CAP_PROP_FPS, 15)

#                 while True:
#                     if cap.isOpened():
#                         self.cam_state[ns], self.src[ns] = cap.read()

#                         # time.sleep(1 / 15)
#                         self.lg.debug('cam opened')

#                         if not self.cam_state[ns]:
#                             self.lg.error(
#                                 f'failed to read camera {ns}/ {source}, retrying..')
#                             break

#                     else:
#                         self.lg.error(f'cannot open cam : {ns} {source}')
#                         time.sleep(1)
#                         break
#                 self.lg.warning(f'releasing recapturing cam {ns}..')
#                 cap.release()
#                 time.sleep(1)

#             except Exception as e:
#                 self.lg.error(f'cannot open cam : {ns}')
#                 self.lg.error(traceback.format_exc())
#                 self.lg.error(e)

#     def detector(self, ns: list = None):
#         ret = [np.empty((0, 2), dtype=int), np.empty((0, 2), dtype=int)]
#         ret_prev = [np.empty((0, 2), dtype=int), np.empty((0, 2), dtype=int)]

#         if ns is None:
#             ns = [0, 1]
#         while True:
#             if self.working_state:
#                 while True:
#                     t0 = time.time()
#                     for t in ns:

#                         if self.cam_state[t]:

#                             t1 = time.time()

#                             # results = self.model.track(self.src[t])
#                             results = self.model(self.src[t], task='detect',
#                                                  verbose=self.cf.getboolean('common', 'yolo_verbose'))
#                             # Visualize the results on the frame
#                             annotated_frame = results[0].plot(
#                                 line_width=1, font_size=0.5, labels=False)
#                             black = np.zeros_like(self.src[t])

#                             for result in results:
#                                 boxes = result.boxes.cpu().numpy()
#                                 for box in boxes:
#                                     # get corner points as int
#                                     r_xyxy = box.xyxy[0].astype(int)
#                                     r_xywh = box.xywh[0].astype(int)

#                                     # draw boxes on img
#                                     # cv2.rectangle(black, r_xyxy[:2],
#                                     #             r_xyxy[2:], (255, 255, 255), 2)

#                                     # cv2.circle(black, (r_xywh[0], r_xywh[1]),
#                                     #         1, (0, 0, 255), 3, cv2.LINE_AA)

#                                     ret[t] = np.append(
#                                         ret[t], [r_xywh[:2]], axis=0)

#                             if ret_prev[t].ndim == 2 and ret[t].ndim == 2:
#                                 self.ret[t] = remove_close_elements(
#                                     ret_prev[t], ret[t], tol=10)

#                                 for r in self.ret[t]:
#                                     if self.DEV:
#                                         cv2.circle(
#                                             black, (r[0], r[1]), 1, (0, 255, 0), 3, cv2.LINE_AA)

#                             if self.DEV:
#                                 res = np.hstack((black, annotated_frame))
#                                 cv2.imshow(f'res_{t}', res)

#                             active_cnt = len(self.ret[t])
#                             # if t ==1:
#                             #     self.lg.warn(f'total_ret {len(ret[t])} {active_cnt=}')
#                             # if active_cnt == 0:
#                             #     self.lg.warning(f'{active_cnt=}')

#                             ############ BDD START CONDITION ########################
#                             # starts detection when the detection is more than 5
#                             # self.lg.debug(f'{self.bdd_start[0]=} {active_cnt=} {int(self.cf.get("ioss","count_threshold").split(",")[0])=} {time.time() - self.bdd_start[1]=}')
#                             if (not self.bdd_start[t]['state']) and active_cnt > int(
#                                     self.cf.get('ioss', 'count_threshold').split(',')[0]) and time.time() - \
#                                     float(self.bdd_start[t]['time']) > 10:
#                                 self.bdd_start[t]['state'] = True
#                                 self.bdd_start[t]['time'] = time.time()

#                                 self.lg.debug(
#                                     f'detect started , cnt : {active_cnt}')
#                                 self.bdd_start[t]['det_id'] = str(uuid.uuid4())
#                                 formatted_time = datetime.now().strftime("%y%m%dT%H%M%S")
#                                 self.start_title = f"{self.cf.get('common', 'device_id')}_{t}_{formatted_time}"
#                                 save_img(img_title=f'{self.start_title}_start',
#                                          detection_path=os.path.join(
#                                              os.getenv('IODEV_PATH'), 'detections', f'cam{t}'),
#                                          max_save_count=self.cf.getint('common', 'max_save_count'), src=annotated_frame)

#                                 # keep_video counts under the restriction
#                                 self.video[t] = save_stream(stream_title=f'{self.start_title}.mp4', path=os.path.join(os.getenv('IODEV_PATH'), 'streams', f'cam{t}'),
#                                                             max_save_count=self.cf.getint('common', 'max_save_count'))

#                                 # sends signal
#                                 start_buf = {"target": "DetectionEventHandler",
#                                              "action": "bdd_start",
#                                              "cam": t,
#                                              "det_id": self.bdd_start[t]['det_id'],
#                                              "img_title": f'{self.start_title}_start',
#                                              "count": active_cnt,
#                                              }
#                                 send_signal(self.classname, start_buf)

#                                 pass

#                             #  in bdd start state
#                             if self.bdd_start[t]['state']:

#                                 if self.video[t] is not None:
#                                     if self.video[t].isOpened():
#                                         # self.lg.error(f'{ns} : failed to open file for save stream!')
#                                         # saves stream
#                                         self.video[t].write(self.src[t])

#                                 # checks max count
#                                 if active_cnt > self.bdd_start[t]['max_cnt']:
#                                     self.bdd_start[t]['max_cnt'] = active_cnt

#                                 #  a conditon that checks time
#                                 time_elasped = time.time() - \
#                                     float(
#                                     self.bdd_start[t]['time']) > 5

#                                 # a condition that checks if birds are exterminated
#                                 sparse_detected = active_cnt < int(
#                                     self.cf.get('ioss', 'count_threshold').split(',')[1])

#                                 # or 30s elasped
#                                 time_elasped_long = time.time(
#                                 ) - float(self.bdd_start[t]['time']) > 30

#                                 ############ BDD END CONDITION ########################

#                                 if (time_elasped and sparse_detected) or time_elasped_long:
#                                     # writing single frame
#                                     formatted_time = datetime.now().strftime("%y%m%dT%H%M%S")
#                                     img_title = f"{self.cf.get('common', 'device_id')}_{t}_{formatted_time}"
#                                     save_img(img_title=f'{img_title}_end',
#                                              detection_path=os.path.join(os.getenv('IODEV_PATH'), 'detections',
#                                                                          f'cam{t}'),
#                                              max_save_count=self.cf.getint(
#                                                  'common', 'max_save_count'),
#                                              src=annotated_frame)

#                                     # sending signal
#                                     end_buf = {"target": "DetectionEventHandler",
#                                                "action": "bdd_end",
#                                                "cam": t,
#                                                "det_id": self.bdd_start[t]['det_id'],
#                                                "start_stream_title": f'{self.start_title}',
#                                                "img_title": f'{img_title}_end',
#                                                "count": self.bdd_start[t]['max_cnt'],
#                                                }
#                                     send_signal(
#                                         f'{self.classname}_end', end_buf)

#                                     # reset params
#                                     self.lg.debug(
#                                         f'detection ended , cnt : {active_cnt}')
#                                     self.bdd_start[t]['state'] = False
#                                     self.bdd_start[t]['time'] = time.time()
#                                     self.bdd_start[t]['max_cnt'] = 0
#                                     self.video[t].release()
#                                     self.video[t] = None

#                             ret_prev[t] = ret[t]
#                             ret[t] = np.empty((0, 2), dtype=int)

#                             if self.DEV and cv2.waitKey(10) & 0xFF == ord('q'):
#                                 cv2.destroyAllWindows()
#                                 break

#                             self.perf[t] = t1 - time.time()

#                         else:
#                             if self.src[t] is not None:
#                                 self.lg.error(
#                                     f' bad cam {t} input : {self.cam_state[t]=} {self.src[t].shape}')

#                             else:
#                                 self.lg.error(
#                                     f' bad cam {t} input : {self.cam_state[t]=} {type(self.src[t])}')
#                             time.sleep(3)

#                 if time.time() - self.perf_timer[t] > 120:
#                     self.lg.debug(
#                         f'HEALTH_CHECK : performance : cam0-{self.perf[0]:.3f}fps, cam1-{self.perf[1]:.3f}fps, total-{t0-time.time:.3f}fps')
#                     self.perf_timer[t] = time.time()

#             else:
#                 self.lg.debug('sleeping due to False working state...')
#                 time.sleep(1)

#     def viewer(self, ns: list = None):
#         if ns is None:
#             ns = [0, 1]
#         while True:
#             for t in ns:
#                 cv2.imshow(f'{t}', self.src[t])

#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 cv2.destroyAllWindows()
#                 break


# if __name__ == '__main__':
#     d = Detector()
#     d.viewer([0])


