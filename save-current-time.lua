start_time = nil

function save_time_handler()
    local time = mp.get_property_osd("time-pos")
    if start_time == nil then
        start_time = time
        mp.osd_message("Start time saved")
    else
        local file = io.open("time.txt", "a")
        file:write(start_time .. "\t" .. time .. "\tXXX\n")
        file:close()
        mp.osd_message("Time saved to time.txt")
        start_time = nil
    end
end
mp.add_key_binding("t", "save_time_handler", save_time_handler)
