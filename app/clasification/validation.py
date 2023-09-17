def validation(file, result, df):
    # Loop over rows
    for index, row in df.iterrows():
        # Loop over columns
        name = df.iloc[index, 0]
        splitName = name.split('.')[0];
        if splitName == file:
            result_s = df.iloc[index, 1]
            df.iloc[index, 2]=str(result)
            if str(result_s).capitalize() != str(result).capitalize():
                print(name, 'problem')
                df.iloc[index, 3]='problem'
            else:
                df.iloc[index, 3] = 'ok'
                print(name, 'ok')