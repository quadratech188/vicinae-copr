#ifndef SATURATE_CAST_FIX_H
#define SATURATE_CAST_FIX_H

#include <numeric>

// saturate_cast was renamed to saturating_cast, but fedora's version of qt6-qtbase-devel didn't get the memo
#if defined(__cpp_lib_saturation_arithmetic) && (__cpp_lib_saturation_arithmetic >= 202603L)
namespace std {
    template <typename R, typename T>
    constexpr R saturate_cast(T x) noexcept {
        return std::saturating_cast<R>(x);
    }
}
#endif

#endif // SATURATE_CAST_FIX_H
