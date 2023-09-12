#include "AP_RangeFinder_config.h"

#include "AP_RangeFinder_Broadcom_AFBR_S50.h"
#include <AP_HAL/AP_HAL.h>

// constructor
AP_RangeFinder_Broadcom_AFBRS50::AP_RangeFinder_Broadcom_AFBRS50(RangeFinder::RangeFinder_State &_state, AP_RangeFinder_Params &_params) :
    AP_RangeFinder_Backend(_state, _params)
{
    _hnd = Argus_CreateHandle();
}

bool AP_RangeFinder_Broadcom_AFBRS50::detect()
{
    return true;
}

void AP_RangeFinder_Broadcom_AFBRS50::update(void)
{

}