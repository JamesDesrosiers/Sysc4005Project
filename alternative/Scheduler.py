import sys

import pandas

from Buffer import Buffer
from ComponentType import ComponentType
from Inspector import Inspector
from RandomGen import exp_rand_gen_range
from Workstation import Workstation
from ProductType import ProductType

if __name__ == "__main__":
    run = {
        'running': True
    }
    num_samples = 300
    i1_c1_timing = exp_rand_gen_range(10.35791, 0.087, 76.284, num_samples).tolist()
    i2_c2_timing = exp_rand_gen_range(15.58843, 0.13, 114.43, num_samples).tolist()
    i2_c3_timing = exp_rand_gen_range(20.63276, 0.031, 104.02, num_samples).tolist()
    ws1_timing = exp_rand_gen_range(4.604417, 0.007, 29.375, num_samples).tolist()
    ws2_timing = exp_rand_gen_range(10.93212, 0.091, 59.078, num_samples).tolist()
    ws3_timing = exp_rand_gen_range(8.79558, 0.102, 51.418, num_samples).tolist()

    print(i1_c1_timing)

    b11 = Buffer(ComponentType.C1)
    b12 = Buffer(ComponentType.C1)
    b13 = Buffer(ComponentType.C1)
    b22 = Buffer(ComponentType.C2)
    b23 = Buffer(ComponentType.C3)

    i1_c1_timing_copy = i1_c1_timing.copy()
    i1 = Inspector([b11, b12, b13], [i1_c1_timing_copy, i1_c1_timing_copy, i1_c1_timing_copy], run)
    i2 = Inspector([b22, b23], [i2_c2_timing.copy(), i2_c3_timing.copy()], run)

    ws1 = Workstation([b11], ws1_timing.copy(), ProductType.P1, run)
    ws2 = Workstation([b12, b22], ws2_timing.copy(), ProductType.P2, run)
    ws3 = Workstation([b13, b23], ws3_timing.copy(), ProductType.P3, run)

    i1.start()
    i2.start()
    ws1.start()
    ws2.start()
    ws3.start()

    while run['running']:
        pass

    print('done')
    print('Num Products')
    print(len(ws1.get_products()))
    print(len(ws2.get_products()))
    print(len(ws3.get_products()))

    # print(i1.get_time_blocked())
    # print(i2.get_time_blocked())
    # print(ws1.get_time_blocked())
    # print(ws2.get_time_blocked())
    # print(ws3.get_time_blocked())

    # Process report summary
    print('Generating Report File\n')
    report_dict = {
        'Workstation 1 Products': [str(len(ws1.get_products()))],
        'Workstation 2 Products': [str(len(ws2.get_products()))],
        'Workstation 3 Products': [str(len(ws3.get_products()))],
        'Inspector 1 Blocked Time': [str(i1.get_time_blocked())],
        'Inspector 2 Blocked Time': [str(i2.get_time_blocked())],
        'Workstation 1 Blocked Time': [str(ws1.get_time_blocked())],
        'Workstation 2 Blocked Time': [str(ws2.get_time_blocked())],
        'Workstation 3 Blocked Time': [str(ws3.get_time_blocked())],
    }
    report_df = pandas.DataFrame.from_dict(report_dict)
    report_df.to_csv('report_summary.csv')

    # Process input info
    print('Generating Input File\n')
    input_dict = {
        'Inspector 1 C1': i1_c1_timing,
        'Inspector 2 C2': i2_c2_timing,
        'Inspector 2 C3': i2_c3_timing,
        'Workstation 1': ws1_timing,
        'Workstation 2': ws2_timing,
        'Workstation 3': ws3_timing
    }
    input_df = pandas.DataFrame.from_dict(input_dict)
    input_df.to_csv('rand_inputs.csv')

    print('Generating Workstation 1 File\n')
    w1_dict = {
        'Product 1 Finish Time': [],
    }
    for product in ws1.get_products():
        w1_dict['Product 1 Finish Time'].append(product.get_finish_time())
    print('WS1 Time:')
    print(sum(w1_dict['Product 1 Finish Time']))
    w1_df = pandas.DataFrame.from_dict(w1_dict)
    w1_df.to_csv('workstation_1.csv')

    print('Generating Workstation 2 File\n')
    w2_dict = {
        'Product 2 Finish Time': [],
    }
    for product in ws2.get_products():
        w2_dict['Product 2 Finish Time'].append(product.get_finish_time())
    print('WS2 Time:')
    print(sum(w2_dict['Product 2 Finish Time']))
    w2_df = pandas.DataFrame.from_dict(w2_dict)
    w2_df.to_csv('workstation_2.csv')

    print('Generating Workstation 3 File\n')
    w3_dict = {
        'Product 3 Finish Time': [],
    }
    for product in ws3.get_products():
        w3_dict['Product 3 Finish Time'].append(product.get_finish_time())
    print('WS3 Time:')
    print(sum(w3_dict['Product 3 Finish Time']))
    w3_df = pandas.DataFrame.from_dict(w3_dict)
    w3_df.to_csv('workstation_3.csv')

    sys.exit(0)
