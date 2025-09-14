def analyze_sleep(hours, quality, sleep_time, wake_time, interruptions):
    sleep_analysis = {}
    sleep_analysis["current_state"] = get_sleep_state(hours, quality, sleep_time, wake_time, interruptions)
    sleep_analysis["improvements"] = get_sleep_improvements(hours, quality, sleep_time, wake_time, interruptions)
    sleep_analysis["consequences"] = get_sleep_consequences(hours, quality, sleep_time, wake_time, interruptions)
    
    return sleep_analysis

def get_sleep_state(hours, quality, sleep_time, wake_time, interruptions):
    state = {}
    
    state["sleep_duration_hours"] = hours
    state["sleep_quality_rating"] = quality
    state["sleep_time"] = sleep_time
    state["wake_time"] = wake_time
    state["interruptions_count"] = interruptions
    
    if hours < 6:
        state["duration_category"] = "Insufficient"
    elif hours < 7:
        state["duration_category"] = "Borderline"
    elif hours <= 9:
        state["duration_category"] = "Optimal"
    else:
        state["duration_category"] = "Extended"
    
    if quality < 3:
        state["quality_category"] = "Poor"
    elif quality < 7:
        state["quality_category"] = "Moderate"
    else:
        state["quality_category"] = "Good"
    
    if interruptions == 0:
        state["continuity"] = "Uninterrupted"
    elif interruptions <= 2:
        state["continuity"] = "Slightly fragmented"
    else:
        state["continuity"] = "Highly fragmented"
    
    return state

def get_sleep_improvements(hours, quality, sleep_time, wake_time, interruptions):
    improvements = []
    
    if hours < 7:
        improvements.append("Aim for 7-9 hours of sleep per night")
    
    if quality < 7:
        improvements.append("Improve sleep environment: dark room, comfortable temperature, reduce noise")
    
    try:
        sleep_hour = int(sleep_time.split(':')[0])
        if sleep_hour < 21 or sleep_hour > 23:
            improvements.append("Try to establish a consistent sleep time between 9pm-11pm")
    except:
        improvements.append("Establish a consistent sleep schedule")
    
    if interruptions > 2:
        improvements.append("Reduce sleep interruptions by limiting liquids before bed and addressing potential sleep disorders")
    
    improvements.append("Establish a relaxing pre-sleep routine without screens 30-60 minutes before bed")
    
    return improvements

def get_sleep_consequences(hours, quality, sleep_time, wake_time, interruptions):
    consequences = []
    
    if hours < 6:
        consequences.append("Chronic sleep deprivation increases risk of heart disease, diabetes, obesity, and reduces immune function")
        consequences.append("Short-term effects include reduced cognitive function, mood disturbances, and increased stress")
    
    if quality < 5:
        consequences.append("Poor sleep quality can cause daytime fatigue, impaired memory, and reduced productivity")
    
    if interruptions > 3:
        consequences.append("Fragmented sleep prevents reaching deep sleep stages, reducing physical recovery and memory consolidation")
    
    try:
        sleep_hour = int(sleep_time.split(':')[0])
        if sleep_hour < 20 or sleep_hour > 2:
            consequences.append("Irregular sleep timing disrupts circadian rhythm, affecting hormone production and metabolic health")
    except:
        pass
    
    return consequences