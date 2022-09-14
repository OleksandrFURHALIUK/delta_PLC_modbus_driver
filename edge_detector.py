import threading
from threading import Thread
from time import sleep


class EdgeDetector(threading.Thread):
    def __init__(self, tags: dict, period=1):
        Thread.__init__(self, target=self._edge_detection)
        self.name = 'Edge detector thread'
        self._stop_event = threading.Event()
        self.detector_period = period
        self.tags = tags
        self.tags_last_state = dict()
        self.on_rising_edge_func = dict()
        self.on_rising_edge_func_args = dict()
        self.on_falling_edge_func = dict()
        self.on_falling_edge_func_args = dict()

    def start_detecting(self):
        print('Thread started:', self.name)
        self.start()

    def stop_detection(self):
        self._stop_event.set()
        print('Thread stoped:', self.name)

    def start_edge_detector_on_tag(self, tag_name):
        pass

    def stop_edge_detector_on_tag(self, tag_name):
        pass

    def set_on_rising_edge_func(self, tag_name: str, func, *args, **kwargs):
        self.on_rising_edge_func[tag_name] = func
        self.on_rising_edge_func_args[tag_name] = (args, kwargs)

    def set_on_falling_edge_func(self, tag_name: str, func, *args, **kwargs):
        self.on_falling_edge_func[tag_name] = func
        self.on_falling_edge_func_args[tag_name] = (args, kwargs)

    def _edge_detection(self):
        while not self._stop_event.is_set():
            for tag_name, value in self.tags.items():
                clk_bit = self.tags[tag_name]
                print(tag_name, clk_bit)

                # rising edge detect
                if clk_bit and not self.tags_last_state[tag_name]:
                    print('Detected rising edge:', tag_name)
                    if self.on_rising_edge_func.get(tag_name):
                        self.on_rising_edge_func.get(tag_name)(*self.on_rising_edge_func_args.get(tag_name)[0],
                                                               **self.on_rising_edge_func_args.get(tag_name)[1])

                # falling edge detect
                if not clk_bit and self.tags_last_state.get(tag_name):
                    print('Detected falling edge:', tag_name)
                    if self.on_falling_edge_func.get(tag_name):
                        self.on_falling_edge_func.get(tag_name)(*self.on_falling_edge_func_args.get(tag_name)[0],
                                                                **self.on_falling_edge_func_args.get(tag_name)[1])
                self.tags_last_state[tag_name] = clk_bit
            sleep(self.detector_period)


def main():
    tags = {'Tag_name 1': False,
            'Tag_name 2': False,
            'Tag_name 3': False,
            'Tag_name 4': False,
            'Tag_name 5': False,
            }

    detector = EdgeDetector(tags, period=0.5)
    detector.start_detecting()
    detector.set_on_rising_edge_func('Tag_name 1', print)
    detector.set_on_falling_edge_func('Tag_name 1', print, 'a', 'b', 'c', sep='*')

    counter = 0
    while counter < 5:
        tags['Tag_name 1'] = False
        sleep(1)
        tags['Tag_name 1'] = True
        sleep(1)
        counter += 1
    detector.stop_detection()


if __name__ == '__main__':
    main()
