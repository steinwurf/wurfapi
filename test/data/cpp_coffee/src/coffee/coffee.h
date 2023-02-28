#include <cstdint>
#include <function>
#include <iostream>

namespace project
{
inline namespace v1_0_0
{
namespace coffee
{
/// @brief A machine to brew your coffee. Docs by http://steinwurf.com.
///
/// The coffee machine object serves as your applications entry
/// point for brewing coffee. You have to remember to fill the
/// project::coffee::machine::water_tank though.
///
/// The following links are followed by *punctuations*:
///
/// http://dot.com.
///
/// http://comma.com,
///
/// http://exclamationmark.com!
///
/// http://questionmark.com?
///
/// http://colon.com:
///
/// http://semicolon.com;
///
/// http://backslash.com/ **nothing** should happen here.
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
        ///    sound an alarm if the water tank is too full. To disable the
        ///    safety valve set `false`.
        /// @return `true` if the filling was successful otherwise `false`
        bool fill(const cups& number_of_cups, bool safety_valve);

        /// The volume of the water tank.
        double tank_volume;
    };

    /// The generic callback type
    using callback = std::function<void(int cups, uint8_t* data)>;

    /// Another way to define a type is a typedef
    typedef callback other_callback;

    /// A variable which uses the callback using statement
    callback m_callback;

    /// A variable which uses the other_callback typedef statement
    other_callback m_other_callback;

private:
    /// Internal brewing state
    struct brew_state
    {
        bool m_on;
    };

public:
    /// @brief The power state
    enum class power
    {
        /// Turn power on
        on,
        /// Turn power off
        off
    };

    /// Constructor
    machine();

    /// Constructor with power
    machine(power pwr);

    /// Destructor
    ~machine();

    /// Set the power of the machine
    void set_power(power);

    /// @brief Set the number of cups to brew.
    ///
    /// Before setting number of cups, check the following:
    /// 1. You have enough water in the `water_tank`.
    ///     * Of course you also need power.
    ///
    ///           std::cout << "You need power" << std::endl;
    ///           std::cout << "So plug it in" << std::endl;
    ///     * A stable surface is also important!
    ///
    /// 2. Your coffee mug is clean.
    ///
    /// You can see number_cups() for how many cups
    /// See water_tank::fill() for how to fill the water tank.
    /// See the water_tank::tank_volume for the
    /// volume of the tank.
    /// @param cups The number of cups
    void set_number_cups(uint32_t cups = 0);

    /// @copydoc set_number_cups
    void set_number_cups(std::string cups);

    /// @return The number of cups
    virtual uint32_t number_cups() const;

    /// @brief The version of the machine
    ///
    /// Example:
    ///
    ///     std::cout << "The version";
    ///               << project::coffee::machine::version() << "\n";
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

    /// Get the first water tank
    const water_tank& tank() const;

    /// Get the first water tank
    water_tank& tank();

    /// Get all water tanks
    std::vector<water_tank> tanks();

    /// Add a generic beans
    ///
    /// @tparam Beans The generic bean type
    /// @tparam BeanSize The size of a bean
    template <class Beans = Arabica, uint32_t BeanSize = 100>
    void add_beans(const Beans& beans);

    /// Get the number of beans needed for a given mug
    auto get_bean_count(mug_size size_of_mug) const -> uint32_t;

    /// Get the last cup of coffee
    auto get_last_cup() const;

    /// The number of cups brewed by this machine.
    uint32_t cups_brewed = 0;

    /// The number of cups brewed by all machines.
    static uint32_t total_cups_brewed;

    /// This header is coffee.h if this is important? Also there is an example
    /// in header.h
    /// @return the mug_size
    mug_size mug_size() const;

    /// Set the machine name
    void set_name(const char name[40]);

protected:
    /// @brief Set the heat.
    ///
    /// This function is use to set the head of the machine.
    ///
    void set(const heat& h, int max) const;

private:
    void help_brew();

private:
    struct impl;
    std::unique_ptr<impl> m_impl;
};

/// @brief A genric cup
/// @tparam T The liquid for the cup
/// @tparam Liter The number of liters
template <class T = water, uint32_t Liter>
struct cup
{
    /// The liquid contained
    T m_liquid;
};

/// @brief A tea cup
/// @tparam Liter The number of liters
template <uint32_t Liter>
struct cup<tea, Liter>
{
    /// The liquid contained
    tea m_liquid;
};

/// @brief A 5 liter tea cup
template <>
struct cup<tea, 5>
{
    /// The liquid contained
    tea m_liquid;
};

}

/// @brief Prints the `a` and then the value pointed to by `b`.
///
/// This is really handy in case you need to see them.
///
/// Example:
///
///     std::cout << project::coffee::print(2.0, &value) << "\n";
///
/// Remember to use `\n` rather than `std::endl` it is more
/// efficient.
///
/// @param a A is actually a double.
/// @param b Whereas b is a pointer to an int.
/// @return This does not really return anything because
///         it is `void` but it could!
void print(double a, int* b);

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
}

/// @return The version of the library as a string
std::string version();

/// The coffee version
#define COFFEE_VERSION "1.0.0"
