from geopy.distance import vincenty


def return_list_of_distance(start_latitude, start_longitude, institution_queryset):
    list_result = []
    for institution in institution_queryset:
        distance = vincenty((start_latitude, start_longitude), (institution.latitude,institution.longitude)).meters
        list_result.append((institution, distance))

    list_result.sort(key=lambda item: item[1])

    return list_result
