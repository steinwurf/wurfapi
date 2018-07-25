#include <cstdint>
#include <iostream>

namespace project
{
namespace coffee
{
/// @brief A machine to brew your coffee.
///
/// The coffee machine object serves as your applications entry
/// point for brewing coffee. You have to remember to fill the
/// project::coffee::machine::water_tank though.
class machine
{
public:
    /// @brief The water thank
    struct water_tank
    {
        /// @return `true` if the water tank is full otherwise `false`.
        bool is_full() const;

        /// @param number_of_cups Fill the water tank with the specified number
        ///     number of cups.
        /// @param safety_valve Set `true` to enable the safety valve this will
        ///    sound and alarm if the water tank is too full. To disable the
        ///    safety valve set `false`.
        /// @return `true` if filling was successfull otherwise `false`
        bool fill(const cups& number_of_cups, bool safety_valve);
    };

    /// @brief Set the number of cups to brew.
    ///
    /// You can see number_cups() for how many cups
    /// @param cups The number of cups
    void set_number_cups(uint32_t cups);

    /// @copydoc set_number_cups
    void set_number_cups(std::string cups);

    /// @return The number of cups
    virtual uint32_t number_cups() const;

    /// @brief The version of the machine
    ///
    /// Example:
    ///
    ///     std::cout << "The version";
    ///                << project::coffee::machine::version() << "\n";
    ///
    /// Remember to use `\n` rather than `std::endl` it is more
    /// efficient.
    ///
    /// @return The version of the machine.
    /// Example:
    ///
    ///     std::cout << machine::version();
    ///     std::cout << "\n";
    ///
    static std::string version();

protected:
    /// @brief Set the heat.
    ///
    /// This function is use to set the head of the machine.
    ///
    void set(const heat& h, int max) const;

private:
    void help_brew();
};
}

void print(double a);
void print(int a);
}

std::string version();
