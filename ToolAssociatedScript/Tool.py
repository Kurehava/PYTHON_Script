from os import system
from re import compile
from sys import exit, platform
from time import sleep
from random import seed, random, choice

import numpy as np
from pandas import read_csv as rdc
from pyfiglet import figlet_format as ff

# define  input_file -> ipf
# define output_file -> opf
erro = '\033[31m[ERROR]\033[0m'
info = '\033[32m[INFO_]\033[0m'
warn = '\033[33m[WARN_]\033[0m'

def ddd(not_ddd_list):
    # data_de_duplication
    return list(set(not_ddd_list))

def age_layering_v1(ipf, opf):
    df = rdc(ipf, header=None)
    df.iloc[:, 0] = df.iloc[:, 0] // 10 * 10
    df.to_csv(opf, index=None, header=None)

def average_v1(ipf, opf, rows):
    df = rdc(ipf, header=None)
    row_list = [int(c) for c in rows.split('_')]
    
    avg = df.iloc[row_list, :].mean().astype(int)
    for i in range(len(row_list)):
        df.iloc[row_list[i]] = avg
    
    df.to_csv(opf, index=None, header=None)

def bottom2_round_v1(ipf, opf, cols, epsilons):
    df = rdc(ipf, header=None)
    col__list = [int(c) for c in cols.split('_')]
    chop_list = [int(c) for c in epsilons.split('_')]
    
    for i in range(len(col__list)):
        df.iloc[
            df.iloc[:, cols[i]] <= chop_list[i],
            col__list[i]
        ] = chop_list[i]
    
    df.to_csv(opf, index=None, header=None)

def exclude_v1(ipf, opf, target_rows):
    df = rdc(ipf, header=None)
    exclude_row_list = [int(i) for i in target_rows.split('_')]
    df = df.drop(index=df.index[exclude_row_list])
    df.to_csv(opf, index=None, header=None)

def kanony_v1(ipf, opf, cols, k):
    def kanony(k_df, k_qi, k_k):
        return k_df.groupby(k_qi).filter(lambda x: x[0].count() >= k_k)

    df = rdc(ipf, header=None)
    qi = ddd([int(i) for i in cols.split('_')])
    
    anonymized_df = kanony(df, qi, k)
    anonymized_df.to_csv(opf, index=None, header=None)

def lap_v2(ipf, opf, cols, epsilons, random_seed):
    def lap(x, eps, seed):
        x += np.random.default_rng(seed).laplace(0, 1/eps, x.shape[0])
        return ((x * 2 + 1) // 2).astype(int)

    def lapdf(dfin, lcol__list, lepss_list, SEED):
        df = dfin.copy()
        for i in range(len(cols)):
            df.iloc[:, lcol__list[i]] = lap(df.iloc[:, col__list[i]], lepss_list[i], SEED)

    SEED = random_seed
    np.random.seed(SEED)
    df = rdc(ipf, header=None)
    col__list = [int(c) for c in cols.split('_')]
    epss_list = [float(e) for e in epsilons.split('_')]
    
    for i in range(len(cols)):
        df.iloc[:, col__list[i]] = lapdf(
            df.iloc[:, col__list[i]], epss_list[i], SEED
            )
    df.to_csv(opf, index=None, header=None)

def nn_v1(ipf, opf, rows, cols):
    df = rdc(ipf, header=None)
    row_list = [int(r) for r in rows.split('_')]
    col_list = [int(c) for c in cols.split('_')]
    
    for i in range(len(cols)):
        df.iloc[row_list[i], col_list[i]] = 99
    df.to_csv(opf, index=None, header=None)

def rr_v1(ipf, opf, prob, cols, random_seed):
    def rr(x, q):
        uniq = x.value_counts().index.values
        y = [i if random() < q else choice(uniq) for i in x]
        return y
    def rrdf(df, q, target):
        df = df.copy()
        for i in target:
            df2.iloc[:, i] = rr(df.iloc[:, i], q)
        return df2
    seed(int(random_seed))
    df = rdc(ipf, header=None)
    q = float(prob)
    target = ddd([int(t) for t in cols.split('_')])
    df2 = rrdf(df, q, target)
    df.to_csv(opf, header=None, index=None)

def shuffle_v1(ipf, opf, random_seed):
    df = rdc(ipf, header=None)
    df2 = df.sample(frac=1, random_state=random_seed)
    df2.to_csv(opf, header=None, index=None)

def top2_round_v1(ipf, opf, cols, epsilons):
    df = rdc(ipf, header=None)
    col__list = [int(c) for c in cols.split('_')]
    chop_list = [int(e) for e in epsilons.split('_')]
    
    for i in range(len(cols)):
        df.iloc[
            df.iloc[:, col__list[i]] >= chop_list[i],
            col__list[i]
        ] = chop_list[i]
    df.to_csv(opf, header=None, index=None)

def param_input(method_list, param_type):
    if len(method_list) != len(param_type):
        print(f'{erro}Inconsistent number of methods and parameters.')
        print(f'{erro}Plz reinput.')
        return [0]
    print(f'Method {menu_list[select - 1]} parameter input:')
    pi_count = 1
    input_fail = []
    # while 轮询fail数组的第一个项目
    list_max = len(max(method_list, key=len))
    formatpi = list_max if list_max <= 11 else 11
    value_temps = []
    print(f'{space * 7}Method Name {space * (formatpi - 11)} Parameter Value')
    for index in range(len(method_list)):
        mp, tp = method_list[index], param_type[index]
        print(f'No.{pi_count if pi_count > 10 else f"0{pi_count}"}: ', end='')
        print(f'{mp if len(mp) <= formatpi else f"{mp}{space * (formatpi - len(mp))}"} ')
        temp = input()
        if check_str(temp):
            str_type = 'float' if '.' in temp else 'int'
        else:
            str_type = 'str' if '_' in temp else 'None'
        
        pi_count += 1
        value_temps.append(input())
    return [1, value_temps]

def exit_tool():
    exit(0)

def check_str(string):
    return bool(compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(string))

def banner_():
    banner = f'\033[41;30miPWS 統合ツール \033[0;0m\n'\
             f'Powered by \033[96mSHO\033[0m \n'\
             f'Based \033[92miPWS Offical Tools \033[0m\n'\
             f'\033[33m{"=" * 50}\n{ff("iPWS Tools")}{"=" * 50}\033[0m'
    print(banner)
    count = 0
    for ml in menu_list:
        count += 1
        print(f'{count if count >= 10 else f"0{count}"}. \033[96m{ml}\033[0m')

if __name__ == '__main__':
    while True:
        system('clear') if platform in {'linux', 'darwin'} else system('cls')
        menu_list = [
            'age_layering_v1',
            'average_v1',
            'bottom2_round_v1',
            'exclude_v1',
            'kanony_v1',
            'lap_v2',
            'nn_v1',
            'rr_v1',
            'shuffle_v1',
            'top2_round_v1',
            'exit_tool'
        ]
        space = ' '
        banner_()
        try:
            select = int(input('>> ').strip('"').strip(' ').strip('\''))
            globals()[menu_list[select - 1]]()
            input('continue? >> ')
        except Exception as E:
            print(f"{erro}: Illegal input")
            print(f"{erro}: Please enter only numbers")
            for i in range(3, 0, -1):
                print(f'\rwait {i} sec.', end='')
                sleep(1)
