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
///
uint32_t set(const heat& h, int max) const;

/// Test array parameters
/// @param array The name of the heat source as a const array
void set_array(const uint8_t array[100]) const;

/// Test default parameters
/// @param test Testing bools
void set_bool(bool test = false);

/// Test convoluted stuff
void set_stuff(int (*(*x)(double))[3] = nullptr);