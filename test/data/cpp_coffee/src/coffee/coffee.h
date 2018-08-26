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
    /// Before setting number of cups, check the following:
    /// 1. You have enough water in the `water_tank`.
    ///     * Of course you also need power.
    ///
    ///           std::cout << "You need power" << std::endl;
    ///           std::cout << "So plug it in" << std::endl;
    ///
    /// 2. Your coffee mug is clean.
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

    /// Get the water tank
    water_tank tank();

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

/// @brief Prints the `a` and then the `b`.
///
/// This is really handy in case you need to see them.
///
/// Example:
///
///     std::cout << project::coffee::print(2.0, 1) << "\n";
///
/// Remember to use `\n` rather than `std::endl` it is more
/// efficient.
///
/// @param a A is actually a double.
/// @param b Whereas b is an int.
/// @return This does not really return anything because
///         it is `void` but it could!
void print(double a, int b);

/// @param a_number This is the most important parameter.
///     Without it the function will not work.
///     Example:
///
///         project::coffee::print(3);
///     Does this work
///
/// @param on_paper If `true` print on some actual paper.
void print(int a_number, bool on_paper);
}

std::string version();
