#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Calculation of frequency response and filter coefficient @yaku
# Filter Design with Parks-McClellan Remez
# https://github.com/ShigeoYakuno/REMEZ_FIR_FILTER

import tkinter as tk
import tkinter.font as f
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import re

POS_TEXT_X_OFS = 200
POS_TEXT_Y_OFS = 50


class Application(tk.Frame):
    # entry Widget val
    entry = None

    # Function called when input restriction fails
    def invalidText(self):
        print("restriction fails !")

    def onValidate(self, S):
        # If the entered characters are half-width numbers
        if re.match(re.compile("[0-9]+"), S):
            return True
        elif re.match(re.compile("[.]+"), S):
            return True
        else:
            return False

    def calclate_fir(self):
        fs = float(self.rate_entry.get())  # Sample rate, Hz
        cutoff = float(self.cutoff_entry.get())  # Desired cutoff frequency, Hz
        trans_width = float(self.tranwith_entry.get())  # pass band to stop band, Hz
        numtaps = int(self.taps_entry.get())  # Size of the FIR filter.

        desired = [
            1.0,
            0.000,
        ]  # Desired gain for each of the bands: 1 in the pass band, 0 in the stop band
        print("----------settings----------")
        print(
            f"rate={fs} SPS cutoff={cutoff} Hz tranwidth={trans_width} Hz taps={numtaps}"
        )

        remez_impres = sp.signal.remez(
            numtaps, [0, cutoff, cutoff + trans_width, 0.5 * fs], desired, fs=fs
        )  # taps
        remez_freq, remez_fresponse = sp.signal.freqz(
            remez_impres, [1], worN=2000
        )  # w,h
        # remez_amp = np.abs( remez_fresponse )

        # Dump the coefficients for comparison and verification
        print("----------filter coef----------")
        print("")
        for ii in range(numtaps):
            # print(' tap %2d   %-3.11f ' % (ii+1, remez_impres[ii]))
            print("%-3.11f" % (remez_impres[ii]))
        print("")
        print("-----------end-----------")

        # plot frequency response figure
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(0.5 * fs * remez_freq / np.pi, 20 * np.log10(np.abs(remez_fresponse)))
        ax.set_ylim(-80, 5)
        ax.set_xlim(0, 0.5 * fs)
        # ax.set_xlim(0, 20)
        # ax.set_xticks([0, 2,4,6,8,10,12,14,16,18,20])
        ax.grid(True)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Gain (dB)")
        ax.set_title("Frequency Response")

        plt.show()

    def __init__(self, master=None):
        # init to Window
        super().__init__(master)

        self.master.title(
            "Fir Filter Using Remez algorithm calculation tools Ver1.0 @yaku"
        )
        self.master.geometry("800x400")

        frame = tk.Frame(self.master)
        frame.pack()

        # Register a function to restrict input.
        # Required to link parameters and functions.
        vcmd = self.register(self.onValidate)

        font1 = f.Font(family="Lucida Console", weight="bold", size=36, slant="italic")
        font2 = f.Font(family="Lucida Console", weight="bold", size=22, slant="italic")
        font3 = f.Font(family="Lucida Console", weight="bold", size=10, slant="italic")

        rbl_pos_x = 10
        txt_pos_x = 20
        rbl_pos_y = 10
        txt_pos_y = 30

        # sampling rate box
        self.rate_rabel = tk.Label(root, text="sampling rate(Hz)", font=font3)
        self.rate_rabel.place(x=rbl_pos_x, y=rbl_pos_y)

        # Create an entry widget using frame widget (Frame) as the parent element.
        self.rate_entry = tk.Entry(
            root,
            width=15,
            validate="key",
            validatecommand=(vcmd, "%S"),
            invalidcommand=self.invalidText,
        )
        self.rate_entry.place(x=txt_pos_x, y=txt_pos_y)
        # self.rate_entry.pack()

        rbl_pos_x = rbl_pos_x + POS_TEXT_X_OFS
        txt_pos_x = txt_pos_x + POS_TEXT_X_OFS

        # cutoff frequency
        self.cutoff_rabel = tk.Label(text="cut off (Hz)", font=font3)
        self.cutoff_rabel.place(x=rbl_pos_x, y=rbl_pos_y)

        self.cutoff_entry = tk.Entry(
            root,
            width=15,
            validate="key",
            validatecommand=(vcmd, "%S"),
            invalidcommand=self.invalidText,
        )
        self.cutoff_entry.place(x=txt_pos_x, y=txt_pos_y)

        rbl_pos_x = rbl_pos_x + POS_TEXT_X_OFS - 40
        txt_pos_x = txt_pos_x + POS_TEXT_X_OFS - 40

        # transition width
        self.tranwith_rabel = tk.Label(text="transition width (Hz)", font=font3)
        self.tranwith_rabel.place(x=rbl_pos_x, y=rbl_pos_y)

        self.tranwith_entry = tk.Entry(
            root,
            width=15,
            validate="key",
            validatecommand=(vcmd, "%S"),
            invalidcommand=self.invalidText,
        )
        self.tranwith_entry.place(x=txt_pos_x, y=txt_pos_y)

        rbl_pos_x = rbl_pos_x + POS_TEXT_X_OFS + 20
        txt_pos_x = txt_pos_x + POS_TEXT_X_OFS + 20

        # number of taps
        self.taps_rabel = tk.Label(text="number of taps(num)", font=font3)
        self.taps_rabel.place(x=rbl_pos_x, y=rbl_pos_y)

        self.taps_entry = tk.Entry(
            root,
            width=15,
            validate="key",
            validatecommand=(vcmd, "%S"),
            invalidcommand=self.invalidText,
        )
        self.taps_entry.place(x=txt_pos_x, y=txt_pos_y)

        # calcurate button
        self.calc_btn = tk.Button(
            root, text="CALCURATE", font=font2, command=self.calclate_fir
        )
        self.calc_btn.place(x=400, y=300)

        self.expla_rabel = tk.Label(
            root,
            text="transition width is frequency of pass band to stop band ",
            font=font3,
        )
        self.expla_rabel.place(x=10, y=100)


if __name__ == "__main__":
    # maike a window
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
