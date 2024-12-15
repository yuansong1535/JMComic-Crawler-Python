from jmcomic import *
from jmcomic.cl import JmcomicUI

# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
jm_albums = '''
6349
1030692
1030843
1030851
1031042
1031341
1031349
187420
187
222663
198117
151959
230806
1022543
1023592
1023975
1024197
1025627
1025664
1026274
1026839
1026999
1027119
1027524
1027670
1027955
1028376
1028412
1028415
1028486
1028490
1028992
639937
363869
589343
587915
1022073
1021282
1021128
578526
44230
251137
253895
393485
485647
374837
346610
461641
346862
362057
544490
396284
429505
394449
195530
436319
570083
366517
225671
537172
376305
411311
373099
377954
386471
369599
551529
565620
403508
267805
400312
225346
445794
363033
262147
507769
273120
224412
498861
1019838
1016515
1019278
1019260
1019073
1018734
1018594
1018592
583216
413166
588829
580897
454826
316721
402929
1018338
1018336
1018181
1018057
1017655
1017653
1017571
1017436
1017435
1017177
1016810
1016801
1016796
1016521
1016491
1015683
651309
651388
1013201
1012969
1013159
1013165
1013527
1014570
1014707
1014802
1014710
1015387
1015388
243109
134
259565
146860
1013087
517748
533291
649004
649003
649488
650145
650172
650578
650872
650873
650886
651311
651326
651405
651408
651777
651723
651821
652082
1012642
1012702
1012712
1012750
1012961
1012968
587763
607101
652015
649487
649576
644090
644183
645596
645636
648459
648430
648474
648281
648248
646425
647444
644854
645836
646435
512524
644798
346346
643764
643777
371570
395286
394523
401496
544360
547094
643305
643128
527737
642949
642796
632772
634758
636724
637897
638152
638205
639575
641346
641355
641356
641358
641359
641360
641361
640767
62343
79040
208011
243919
487301
512471
639760
639762
640288
640352
640474
641147
641840
638495
638686
639022
639596
639756
640292
640289
640712
641143
641172
641301
641324
641332
641333
641315
641740
641731
428372
392330
473417
417463
442179
501838
255
629136
629862
630623
630631
631161
631337
636701
636717
637105
637758
638243
637379
619258
619491
621912
625778
626341
626334
626343
626561
627089
627098
629135
629875
631835
634130
635416
635860
635969
632810
629265
630352
632073
632536
629866
544388
627665
627766
623269
628554
628595
417689
527782
537167
151138
282516
314934
451610
52500
148632
98780
90772
99981
123418
373213
28273
114397
198681
92587
98910
102769
100092
103663
104799
105245
137920
100409
239794
325752
368595
386001
403075
432840
496898
522421
535059
539284
540167
609430
33982
97363
129681
213232
180488
381987
301447
104663
543525
545733
556526
564071
570981
593472
261254
203445
119
554934
601985
221
616260
616328
617033
617923
619508
620808
623120
620896
623190
625494
625225
621915
623569
623613
623625
527941
589351
595981
419643
438522
465604
600588
600550
601726
601745
601875
601259
123403
560401
562243
150232
244658
146168
1148
556773
556832
557569
554780
555290
532909
547590
552816
554707
316181
506255
547228
179669
543977
544401
544526
544922
546306
546716
545437
537119
539269
396749
539291
511356
529757
317100
320219
363851
303002
304763
305544
309115
309923
315273
317090
41262
12610
74998
122291
48063
95006
95008
95009
324493
95007
66128
534074
533198
530572
530547
529318
527948
527938
527930
435164
383745
325297
511010
113831
59788
467116
433649
427728
331731
318202
330919
333209
334717
337881
335762
426980
481536
514711
529618
531606
532361
293094
279762
149080
337219
135520
32001
12620
203611
206893
188593
218862
263461
208112
5004
206818
10542
226647



'''

# 单独下载章节
jm_photos = '''



'''


def env(name, default, trim=('[]', '""', "''")):
    import os
    value = os.getenv(name, None)
    if value is None or value == '':
        return default

    for pair in trim:
        if value.startswith(pair[0]) and value.endswith(pair[1]):
            value = value[1:-1]

    return value


def get_id_set(env_name, given):
    aid_set = set()
    for text in [
        given,
        (env(env_name, '')).replace('-', '\n'),
    ]:
        aid_set.update(str_to_set(text))

    return aid_set


def main():
    album_id_set = get_id_set('JM_ALBUM_IDS', jm_albums)
    photo_id_set = get_id_set('JM_PHOTO_IDS', jm_photos)

    helper = JmcomicUI()
    helper.album_id_list = list(album_id_set)
    helper.photo_id_list = list(photo_id_set)

    option = get_option()
    helper.run(option)
    option.call_all_plugin('after_download')


def get_option():
    # 读取 option 配置文件
    option = create_option(os.path.abspath(os.path.join(__file__, '../../assets/option/option_workflow_download.yml')))

    # 支持工作流覆盖配置文件的配置
    cover_option_config(option)

    # 把请求错误的html下载到文件，方便GitHub Actions下载查看日志
    log_before_raise()

    return option


def cover_option_config(option: JmOption):
    dir_rule = env('DIR_RULE', None)
    if dir_rule is not None:
        the_old = option.dir_rule
        the_new = DirRule(dir_rule, base_dir=the_old.base_dir)
        option.dir_rule = the_new

    impl = env('CLIENT_IMPL', None)
    if impl is not None:
        option.client.impl = impl

    suffix = env('IMAGE_SUFFIX', None)
    if suffix is not None:
        option.download.image.suffix = fix_suffix(suffix)


def log_before_raise():
    jm_download_dir = env('JM_DOWNLOAD_DIR', workspace())
    mkdir_if_not_exists(jm_download_dir)

    def decide_filepath(e):
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)

        if resp is None:
            suffix = str(time_stamp())
        else:
            suffix = resp.url

        name = '-'.join(
            fix_windir_name(it)
            for it in [
                e.description,
                current_thread().name,
                suffix
            ]
        )

        path = f'{jm_download_dir}/【出错了】{name}.log'
        return path

    def exception_listener(e: JmcomicException):
        """
        异常监听器，实现了在 GitHub Actions 下，把请求错误的信息下载到文件，方便调试和通知使用者
        """
        # 决定要写入的文件路径
        path = decide_filepath(e)

        # 准备内容
        content = [
            str(type(e)),
            e.msg,
        ]
        for k, v in e.context.items():
            content.append(f'{k}: {v}')

        # resp.text
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)
        if resp:
            content.append(f'响应文本: {resp.text}')

        # 写文件
        write_text(path, '\n'.join(content))

    JmModuleConfig.register_exception_listener(JmcomicException, exception_listener)


if __name__ == '__main__':
    main()
