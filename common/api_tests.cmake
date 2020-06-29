# Adding python tests to cmake
set(REFERENCE_NODE https://api.hive.blog)
set(TEST_NODE http://127.0.0.1:8090)

configure_file("${CMAKE_CURRENT_LIST_DIR}/testbase.py" "${CMAKE_BINARY_DIR}/tests/api_tests/testbase.py" COPYONLY)

macro(ADD_API_TEST api_name test_name)
    set(working_dir ${CMAKE_BINARY_DIR}/tests/api_tests/${api_name})
    configure_file("${CMAKE_CURRENT_SOURCE_DIR}/${test_name}.py" "${working_dir}/${test_name}.py" COPYONLY)
    message(STATUS "Adding ${api_name}/${test_name} to test list")
    set(extra_macro_args ${ARGN})
    list(LENGTH extra_macro_args num_extra_args)
    set(test_parameters ${test_name}.py ${TEST_NODE} ${REFERENCE_NODE} ${working_dir})
    if (${num_extra_args} GREATER 0)
        set(test_parameters ${test_name}.py ${TEST_NODE} ${REFERENCE_NODE} ${working_dir} ${extra_macro_args})
    endif()
    add_test(NAME "${api_name}/${test_name}" COMMAND python3 ${test_parameters} WORKING_DIRECTORY ${working_dir})
    set_property(TEST "${api_name}/${test_name}" PROPERTY LABELS python_tests ${api_name} ${test_name})
endmacro(ADD_API_TEST)