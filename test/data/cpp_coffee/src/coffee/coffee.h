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
    uint32_t number_cups() const;

protected:
    /// @brief Set the heat.
    ///
    /// This function is use to set the head of the machine.
    void set(const heat& h, int max) const;

private:
    void help_brew();
};
}

void print(double a);
void print(int a);
}

std::string version();
