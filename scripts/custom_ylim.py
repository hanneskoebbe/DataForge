def custom_ylim(actual, upper_tolerance, lower_tolerance):
    buffer_perc=0.05
    
    # Berechne das obere und untere Limit – orientiert an beiden Werten
    y_max = max(max(actual), max(upper_tolerance))
    y_min = min(min(actual), max(lower_tolerance))

    # Optionaler Puffer (z. B. 5 %)
    buffer = (y_max - y_min) * buffer_perc

    return([y_min, y_max, buffer])