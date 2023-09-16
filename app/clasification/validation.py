def validation(file, result, df):
    # Loop over rows
    for index, row in df.iterrows():
        # Loop over columns
        name = df.iloc[index, 0]
        splitName = name.split('.')[0];
        if splitName == file:
            result_s = df.iloc[index, 1]
            if str(result_s).upper() != str(result).upper():
                print(name, 'problem')
            #else:
                #print(name, 'ok')