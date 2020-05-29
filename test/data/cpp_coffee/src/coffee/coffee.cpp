#include "coffee.h"

namespace project
{
inline namespace v1_0_0
{
namespace coffee
{
/// Implementation details
struct machine::impl
{
    /// Run the machine
    void run();
};
}
}
}

std::string version()
{
    return "1.0.0";
}