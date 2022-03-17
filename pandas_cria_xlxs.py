from datetime import datetime

import pandas as pd


def diff_month(d1, d2):
    '''Retorna a diferenca de meses entre duas datas '''
    return (d2.year - d1.year) * 12 + d2.month - d1.month


def pandas_cria_xlsx(nome_data_e_hora):
    lst_columns = ['01', 'EMPRESA', '03', 'C/V', '05', '06', 'EMPRESA_ABREV', 'PN/ON', '09', '10', '11', '12', '13', 'TICKER', '15', 'AM/EU', 'STRIKE', 'VCTO', '19']  # noQa E501
    # , usecols=lst_columns
    df = pd.read_csv('./temp/SI_D_SEDE.txt', sep='|', header=None, skiprows=1)

    # df = df.drop(df.index[0])
    # df = df.reset_index()
    df.columns = lst_columns
    df = df.drop(['01', '03', '05', '06', '09', '10', '11', '12', '13', '15', '19'], axis=1)   # noQa E501

    # df_mask=df['EMPRESA']=='PETROBRAS'

    # df_mask=df_mask['PN/ON']=='PN      N2'
    df = df[df[['EMPRESA', 'PN/ON']].isin(['PETROBRAS', 'PN      N2']).all(axis=1)]   # noQa E501

    df['VCTO'] = df['VCTO'].astype(int)
    df['VCTO'] = pd.to_datetime(df['VCTO'], format='%Y%m%d')

    df = df.sort_values(by=['VCTO', 'STRIKE'])

    # df.to_excel(nome_data_e_hora + '.xlsx', index = False)

    df_compra = df[df[['C/V']].isin(['OPCOES COMPRA']).all(axis=1)]



    lst_columns_vendas = ['EMPRESA_V', 'C/V_V', 'EMPRESA_ABREV_V', 'PN/ON_V', 'TICKER_V', 'AM/EU_V', 'STRIKE', 'VCTO']   # noQa E501
    df_venda = df[df[['C/V']].isin(['OPCOES VENDA']).all(axis=1)]

    df_venda.columns = lst_columns_vendas   

    df_merged = pd.merge(df_compra, df_venda)
    df_merged = df_merged.drop(['EMPRESA', 'C/V', 'PN/ON', 'EMPRESA_V', 'C/V_V', 'PN/ON_V', 'AM/EU_V', 'EMPRESA_ABREV'], axis=1)   # noQa E501

    df_merged['BID_C'] = ''
    df_merged['ASK_C'] = ''
    df_merged['BID_V'] = ''
    df_merged['ASK_V'] = ''
    df_merged['VOLUME_C'] = ''
    df_merged['VOLUME_V'] = ''

    df_merged['INTRINSECO_C'] = ''
    df_merged['EXTRINSECO_C'] = ''
    df_merged['DISTANCIA_ATIVO'] = ''
    df_merged['DISTANCIA_PERC'] = ''
    df_merged['INTRINSECO_V'] = ''
    df_merged['EXTRINSECO_V'] = ''
    df_merged['CRIACAO_DADOS'] = ''

    df_merged = df_merged[['EMPRESA_ABREV_V', 'AM/EU', 'TICKER',  'STRIKE', 'BID_C', 'ASK_C', 'INTRINSECO_C', 'EXTRINSECO_C', 'DISTANCIA_ATIVO', 'DISTANCIA_PERC', 'TICKER_V', 'STRIKE', 'BID_V', 'ASK_V', 'INTRINSECO_V', 'EXTRINSECO_V', 'VCTO']]   # noQa E501

    now = datetime.now()

    df_merged['DIAS_VENC'] = (df_merged['VCTO'] - now).astype('timedelta64[D]')

    df_merged['MESES_VENC'] = diff_month(now, df_merged['VCTO'].dt)

    print('\nArquivo criado: ' + nome_data_e_hora + '.xlsx')
    df_merged.to_excel('./temp/' + nome_data_e_hora + '.xlsx', index=False)
