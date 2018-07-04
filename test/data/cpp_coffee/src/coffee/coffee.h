#include <cstdint>
#include <iostream>

namespace project
{
namespace coffee
{
class machine
{
public:
    /// @brief The water thank
    struct water_tank
    {
        bool is_full() const;
        void fill();
    };

    /// @brief Set the number of cups to brew.
    void set_number_cups(uint32_t cups);
    void set_number_cups(std::string cups);

    /// @return The number of cups
    uint32_t number_cups() const;

protected:
    /// @brief Set the heat.
    ///
    /// This function is use to set the head of the machine.
    ///
    ///     void yes();
    ///
    /// But maybe it also does other things?
    ///
    /// @param h Set the heat object.
    ///
    /// Test this break
    ///
    /// @param max The maximum heat value.
    /// @return The current heat.
    ///
    ///     for (uint64_t i = 0; i < 3; ++i)
    ///     {
    ///         std::cout << i << "\n";
    ///     }
    ///
    /// And then some text
    uint32_t set(const heat& h, int max) const;

private:
    void help_brew();
};
}

void print(double a);
void print(int a);
}

std::string version();
