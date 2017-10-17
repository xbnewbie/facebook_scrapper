#conversi jarak
from __future__ import division
def from_mil(mil,ukuran):
    urutan_panjang = {};
    urutan_panjang['mil'] = mil;
    urutan_panjang['km'] = mil * 1.60934;
    urutan_panjang['meter'] = mil * 1609.34;
    urutan_panjang['yard'] = mil * 1760;
    urutan_panjang['feet'] = mil * 5280;
    urutan_panjang['inch'] = mil * 63360;
    urutan_panjang['cm'] = mil * 160934;
    return urutan_panjang[ukuran];

def to_mil(val,ukuran):
    mil=0;
    mil_in = {};
    mil_in['km'] = val / 1.60934;
    mil_in['meter'] = val / 1609.34;
    mil_in['yard'] = val / 1760;
    mil_in['feet'] = val / 5280;
    mil_in['inch'] = val / 63360;
    mil_in['cm'] = val / 160934;
    return mil_in[ukuran]

search = raw_input("contoh 10 km, 10 cm , conversi : ");

to      = raw_input("ke 'cm','inch','feet','yard','m','km','mil' = ");

val = search.split(" ")[0];
ukuran = search.split(" ")[1];

val_in_mil = to_mil(float(val),ukuran);
result = from_mil(val_in_mil,to);
print result;
#apakah konversi ke bawah atau ke atas
