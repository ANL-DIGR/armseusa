import cdsapi
import nexradaws
import os
import sys


def make_a_request(year, month, day):
    request = {'product_type': 'reanalysis',
               'format': 'netcdf',
               'variable': [
                   'divergence', 'fraction_of_cloud_cover', 'geopotential',
                   'potential_vorticity', 'relative_humidity',
                   'specific_cloud_ice_water_content', 'specific_cloud_liquid_water_content', 'specific_humidity',
                   'specific_rain_water_content', 'specific_snow_water_content', 'temperature',
                   'u_component_of_wind', 'v_component_of_wind', 'vertical_velocity',
                   'vorticity'
               ],
               'pressure_level': [
                   '1', '2', '3',
                   '5', '7', '10',
                   '20', '30', '50',
                   '70', '100', '125',
                   '150', '175', '200',
                   '225', '250', '300',
                   '350', '400', '450',
                   '500', '550', '600',
                   '650', '700', '750',
                   '775', '800', '825',
                   '850', '875', '900',
                   '925', '950', '975',
                   '1000'
               ],
               'year': year,
               'month': month,
               'day': day,
               'area': "37.00/-94.00/24.00/-75.00",
               'time': [
                   '00:00', '01:00', '02:00',
                   '03:00', '04:00', '05:00',
                   '06:00', '07:00', '08:00',
                   '09:00', '10:00', '11:00',
                   '12:00', '13:00', '14:00',
                   '15:00', '16:00', '17:00',
                   '18:00', '19:00', '20:00',
                   '21:00', '22:00', '23:00'
               ]
               }

    return request


def get_month(year, month, odir):
    c = cdsapi.Client()
    conn = nexradaws.NexradAwsInterface()
    days = conn.get_avail_days(year, month)
    fls = []
    for day in days:
        print('doing ', day)
        # stage to temp dir
        fname = 'era5_seusa' + year + month + day + '.nc'
        outpath = os.path.join(odir, 'era5', year, month)
        try:
            os.makedirs(outpath)
        except FileExistsError:
            pass  # directory exists

        myreq = make_a_request(year, month, day)

        c.retrieve("reanalysis-era5-pressure-levels",
                   myreq, os.path.join(outpath, fname))
        fls.append(fname)

    return fls


if __name__ == '__main__':

    tyear = sys.argv[1]
    tmonth = sys.argv[2]
    todir = sys.argv[3]
    _ = get_month(tyear, tmonth, todir)

