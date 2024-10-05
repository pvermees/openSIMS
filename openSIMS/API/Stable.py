import math
import pandas as pd
import numpy as np
import openSIMS as S
import matplotlib.pyplot as plt

class Stable:

    def get_csv(self,name):
        sample = self.samples.loc[name]
        settings = S.settings(self.method)
        ions = settings['ions']
        out = pd.DataFrame()
        for ion in ions:
            out[ion] = sample.cps(self.method,ion)['cps']
        return out

    def get_num_den(self):
        settings = S.settings(self.method)
        num = settings['deltaref']['num']
        den = settings['deltaref']['den']
        return num, den

    def get_ratios(self):
        num, den = self.get_num_den()
        ratios = [f"{n}/{d}" for n, d in zip(num, den)]
        return num, den, ratios

    def raw_logratios(self,name):
        raw_cps = self.get_csv(name)
        num, den, ratios = self.get_ratios()
        out = np.log(raw_cps[num]) - np.log(raw_cps[den]).values
        return out.set_axis(ratios,axis=1)

    def offset(self,name):
        standard = self.samples.loc[name]
        num, den, ratios = self.get_ratios()
        settings = S.settings(self.method)
        delta = settings['refmats'][ratios].loc[standard.group]
        return np.log(delta+1)

    def plot(self,fig=None,ax=None):
        num_panels = len(self.pars)
        ratio_names = self.pars.index.to_list()
        nr = math.ceil(math.sqrt(num_panels))
        nc = math.ceil(num_panels/nr)
        if fig is None or ax is None:
            fig, ax = plt.subplots(nrows=nr,ncols=nc)
        lines = dict()
        np.random.seed(0)
        for name, standard in self.samples.items():
            group = standard.group
            if group in lines.keys():
                colour = lines[group]['colour']
            else:
                colour = np.random.rand(3,)
                lines[group] = dict()
                lines[group]['colour'] = colour
                if group != 'sample':
                    lines[group]['offset'] = self.offset(name)
            raw_logratios = self.raw_logratios(name)
            nsweeps = raw_logratios.shape[0]
            logratio_means = raw_logratios.mean(axis=0)
            logratio_stderr = raw_logratios.std(axis=0)/math.sqrt(nsweeps)
            for i, ratio_name in enumerate(ratio_names):
                y_mean = logratio_means.iloc[i]
                y_min = y_mean - logratio_stderr.iloc[i]
                y_max = y_mean + logratio_stderr.iloc[i]
                ax.ravel()[i].scatter(name,y_mean,
                                      s=5,color='black',zorder=2)
                ax.ravel()[i].plot([name,name],[y_min,y_max],
                                   '-',color=colour,zorder=1)
        for i, ratio_name in enumerate(ratio_names):
            title = 'ln(' + ratio_name + ')'
            ax.ravel()[i].set_title(title)
        for group, val in lines.items():
            if group != 'sample':
                y = self.pars + val['offset']
                for i, ratio_name in enumerate(ratio_names):
                    ax.ravel()[i].axline((0.0,y[ratio_name]),slope=0.0,
                                         color=val['colour'],zorder=0)
        for empty_axis in range(len(ratio_names),nr*nc):
            fig.delaxes(ax.flatten()[empty_axis])
        fig.tight_layout()
        return fig, ax

class Calibrator:

    def calibrate(self):
        logratios = self.pooled_calibration_data()
        return logratios.mean(axis=0)

    def pooled_calibration_data(self):
        df_list = []
        for name, standard in self.samples.items():
            logratios = self.raw_logratios(name)
            offset = self.offset(name)
            df = logratios.apply(lambda raw: raw - offset.values, axis=1)
            df_list.append(df)
        return pd.concat(df_list)

class Processor:

    def process(self):
        out = dict()
        for name, sample in self.samples.items():
            logratios = self.raw_logratios(name)
        return out
