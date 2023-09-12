#pragma once

#include "argus.h"

#include "AP_RangeFinder_Backend.h"

class AP_RangeFinder_Broadcom_AFBRS50 : public AP_RangeFinder_Backend
{
public:

    // constructor
    AP_RangeFinder_Broadcom_AFBRS50(RangeFinder::RangeFinder_State &_state, AP_RangeFinder_Params &_params);

    // detect
    static bool detect();

    // update state
    void update(void) override;

private:
    float _distance_m; // stored data

    argus_hnd_t *_hnd;
	argus_mode_t _mode{ARGUS_MODE_SHORT_RANGE}; // Short-Range

protected:
    MAV_DISTANCE_SENSOR _get_mav_distance_sensor_type() const override {
        return MAV_DISTANCE_SENSOR_LASER;
    }
};
