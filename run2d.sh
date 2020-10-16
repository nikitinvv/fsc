for k in {1670..1740..2}; do
python fsc2d_plot_paper.py \
/local/data/vnikitin/Kenan_ZP_8keV_interlaced_5000prj_3s_001/dense_0_0_30.0/results_admm/u/r_0"$k".tiff \
/local/data/vnikitin/Kenan_ZP_8keV_interlaced_5000prj_3s_001/dense_0_1_30.0/results_admm/u/r_0"$k".tiff \
frc"$k".png \
1024 \
5.2 \
0.055 &
done
