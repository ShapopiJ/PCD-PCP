import pandas as pd
import numpy as np
class precip:
    """
    Takes one argument of the dataframe containing monthly data
    """
    def __init__(self, df: pd.DataFrame, datetime_col = "Date Time", columns = None, dateindex = True) -> None:
        """
        Paramters:
        _________
        dateindex: bool
            Is the index a datetime type? If True we need to reset index to work with that index as a DateTime.
        """
        self.df = df
        keys = list(range(1,13))
        values = list(np.arange(0, 360, 30))
        values = np.deg2rad(values)
        self.angles = dict(zip(keys, values))
        self.datetime_col = datetime_col
        self.col = columns
        self.dateindex = dateindex
        self.reset_count = 0
        self.rxyi_count = 0

        #Get columns that will be used
        if self.col == None:
            col = self.df.columns
            self.columns = col
        else:
            self.columns = self.col
        

    def reset_index(self):
        if self.reset_count == 0: # Only run if the index has not yet been reset.
            if self.dateindex:
                self.df = self.df.reset_index()
                self.reset_count += 1
                return self.df
        else:
            print("Index already reset for main DataFrame. Returning same DataFrame")
            return self.df
        

    def get_angle(self, key):
        return self.angles[key]

    def Rxy_i(self):
        if self.rxyi_count == 0:
            #self.columns = self.get_columns()
            self.df = self.reset_index()
            #print(self.datetime_col)
            self.df["angle"] = self.df[self.datetime_col].dt.month.apply(self.get_angle)
            for col in self.columns:
                #print(self.df[self.datetime_col].dt.month)
                self.df[col + "_R_xi"] = self.df[col]*np.sin(
                    np.deg2rad(self.df["angle"]))
                self.df[col + "_R_yi"] = self.df[col]*np.cos(
                    np.deg2rad(self.df["angle"]))
            #print(self.df.head())
            self.rxyi_count += 1
            return #self.df
        else:
            print("Main df already contains Rxi and Ryi computations")
        
    
    def Ri(self):
        self.df = self.reset_index()
        for col in self.columns:
            print(col)
            df = self.df.groupby(self.df[self.datetime_col].dt.year).sum(min_count=1)
        return df


    def PCP(self) -> pd.DataFrame:
        print("Computing PCP")
        self.Rxy_i()
        #df = df.groupby(pd.Grouper(freq="Y")).sum(min_count=1)

        df_PCP = self.df.groupby(self.df[self.datetime_col].dt.year).sum(min_count=1)
        for col in self.columns:
            df_PCP[col + "_PCP"] = np.rad2deg(np.arctan(df_PCP[col + "_R_xi"])/np.arctan(df_PCP[col + "_R_yi"]))
        return df_PCP[[i for i in df_PCP.columns if "PCP" in i]]
    
    def PCD(self):
        print("Computing PCD")
        #print(self.df[self.datetime_col].dtype)
        self.Rxy_i()
        #df = self.Ri() # now each column is a sum of the months in the year
        df_PCD = self.df.groupby(self.df[self.datetime_col].dt.year).sum(min_count=1)
        for col in self.columns:
            df_PCD[col + "_PCD"] = np.sqrt( (df_PCD[col + "_R_xi"]**2) + (df_PCD[col + "_R_yi"]**2) )/df_PCD[col] 
        return df_PCD[[i for i in df_PCD.columns if "PCD" in i]]


if __name__ == "__main__":
    import tools as t
    daily = t.load_dst(file = "../Rainfall_DST_Prod2.csv")
    monthly_sum = daily.groupby(pd.Grouper(freq="M")).sum(min_count=1)
    inst = precip(df = monthly_sum)
    PCP = inst.PCP()
    PCD = inst.PCD()
    PCD.to_csv("PCD.csv")
    PCP.to_csv("PCP.csv")
    