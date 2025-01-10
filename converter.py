from pyproj import CRS, Transformer

MGA2020 = CRS.from_epsg(7856)  # EPSG:7856 is MGA2020 Zone 56
WGS84 = CRS.from_epsg(4326)    # EPSG:4326 is WGS84


def decimal_to_dms(decimal_degree):
    degrees = int(decimal_degree)
    minutes = int(abs(decimal_degree - degrees) * 60)
    seconds = (abs(decimal_degree - degrees) * 60 - minutes) * 60
    return degrees,minutes,seconds

def dms_to_decimal(degrees, minutes, seconds):
    return degrees + minutes / 60 + seconds / 3600

def geo2grid(longitude: float, latitude: float, elevation: float):
    transformer = Transformer.from_crs(WGS84, MGA2020, always_xy=True)
    easting, northing = transformer.transform(longitude, latitude)

    return {
        "Easting": easting,
        "Northing": northing,
        "Elevation": elevation,
    }

def grid2geo(easting: float, northing: float, elevation: float):
    transformer = Transformer.from_crs(MGA2020, WGS84, always_xy=True)
    longitude, latitude = transformer.transform(easting, northing)

    return {
        "Longitude": longitude,
        "Latitude": latitude,
        "Elevation": elevation,
    }

if __name__ == '__main__':
    # Example usage:
    # Receive a list of coordinates in DMS format
    raw_data_dms = [
        [[151,8,57.11845],[-33,56,19.60664],-71.581],
    ]
    for data in raw_data_dms:
        # Convert to decimal format
        longitude = dms_to_decimal(*data[0])
        latitude = dms_to_decimal(*data[1])
        print(geo2grid(longitude, latitude, data[2]))

    # Receive a list of coordinates in decimal format
    raw_data = [
        [328948.782, 6243089.229, -71.581],
    ]
    for data in raw_data:
        print(grid2geo(*data))
        # If needed, convert to DMS format
        # print(decimal_to_dms(grid2geo(*data)["Longitude"]))
        # print(decimal_to_dms(grid2geo(*data)["Latitude"]))