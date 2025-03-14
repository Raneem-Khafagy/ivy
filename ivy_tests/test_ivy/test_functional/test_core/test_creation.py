"""Collection of tests for creation functions."""

# global
from hypothesis import given, strategies as st

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args
from ivy_tests.test_ivy.test_functional.test_core.test_dtype import astype_helper


# native_array
@handle_cmd_line_args
@given(
    dtype_and_x_and_cast_dtype=astype_helper(),
    num_positional_args=helpers.num_positional_args(fn_name="native_array"),
)
def test_native_array(
    *,
    dtype_and_x_and_cast_dtype,
    as_variable,
    num_positional_args,
    native_array,
    instance_method,
    fw,
    device,
):
    input_dtype, x, dtype = dtype_and_x_and_cast_dtype
    helpers.test_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="native_array",
        x=x[0],
        dtype=dtype,
        device=device,
    )


# linspace
@handle_cmd_line_args
@given(
    dtype_and_start_stop=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        num_arrays=2,
        min_value=None,
        max_value=None,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
        allow_inf=False,
        shared_dtype=True,
        large_abs_safety_factor=4,
        small_abs_safety_factor=4,
        safety_factor_scale="log",
    ),
    num=helpers.ints(min_value=1, max_value=5),
    axis=st.none(),
    num_positional_args=helpers.num_positional_args(fn_name="linspace"),
)
def test_linspace(
    *,
    dtype_and_start_stop,
    num,
    axis,
    device,
    num_positional_args,
    fw,
):
    dtype, start_stop = dtype_and_start_stop
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="linspace",
        rtol_=1e-1,
        atol_=1e-2,
        start=start_stop[0],
        stop=start_stop[1],
        num=num,
        axis=axis,
        device=device,
        dtype=dtype[0],
    )


# logspace
@handle_cmd_line_args
@given(
    dtype_and_start_stop=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        num_arrays=2,
        min_value=None,
        max_value=None,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
        shared_dtype=True,
        large_abs_safety_factor=24,
        small_abs_safety_factor=24,
        safety_factor_scale="log",
    ),
    num=helpers.ints(min_value=1, max_value=5),
    base=helpers.floats(min_value=0.1, max_value=10.0),
    axis=st.none(),
    num_positional_args=helpers.num_positional_args(fn_name="logspace"),
)
def test_logspace(
    *,
    dtype_and_start_stop,
    num,
    base,
    axis,
    device,
    with_out,
    num_positional_args,
    fw,
):
    dtype, start_stop = dtype_and_start_stop
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="logspace",
        rtol_=1,  # if It's less than one it'll test for inf
        atol_=1e-06,
        test_values=True,
        start=start_stop[0],
        stop=start_stop[1],
        num=num,
        base=base,
        axis=axis,
        device=device,
    )


# arange
@handle_cmd_line_args
@given(
    start=helpers.ints(min_value=0, max_value=50),
    stop=helpers.ints(min_value=0, max_value=50) | st.none(),
    step=helpers.ints(min_value=-50, max_value=50).filter(
        lambda x: True if x != 0 else False
    ),
    dtype=helpers.get_dtypes("numeric", full=False),
    num_positional_args=helpers.num_positional_args(fn_name="arange"),
)
def test_arange(
    *,
    start,
    stop,
    step,
    dtype,
    device,
    num_positional_args,
    with_out,
    fw,
):
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="arange",
        start=start,
        stop=stop,
        step=step,
        dtype=dtype,
        device=device,
    )


# asarray
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=0,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="asarray"),
)
def test_asarray(
    *,
    dtype_and_x,
    device,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    dtype, x = dtype_and_x

    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="asarray",
        object_in=x,
        dtype=dtype,
        device=device,
    )


# empty
@handle_cmd_line_args
@given(
    shape=helpers.get_shape(
        allow_none=False,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    dtype=helpers.get_dtypes("numeric", full=False),
    num_positional_args=helpers.num_positional_args(fn_name="empty"),
)
def test_empty(
    *,
    shape,
    dtype,
    device,
    num_positional_args,
    fw,
):
    ret = helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="empty",
        shape=shape,
        dtype=dtype,
        device=device,
        test_values=False,
    )
    if not ivy.exists(ret):
        return
    res, res_np = ret
    ivy.set_backend("tensorflow")
    assert res.shape == res_np.shape
    assert res.dtype == res_np.dtype
    ivy.unset_backend()


# empty_like
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="empty_like"),
)
def test_empty_like(
    *,
    dtype_and_x,
    device,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    ret = helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="empty_like",
        x=x[0],
        dtype=dtype,
        device=device,
        test_values=False,
    )
    if not ivy.exists(ret):
        return
    res, res_np = ret
    ivy.set_backend("tensorflow")
    assert res.shape == res_np.shape
    assert res.dtype == res_np.dtype
    ivy.unset_backend()


# eye
@handle_cmd_line_args
@given(
    n_rows=helpers.ints(min_value=0, max_value=10),
    n_cols=st.none() | helpers.ints(min_value=0, max_value=10),
    k=helpers.ints(min_value=-10, max_value=10),
    batch_shape=st.lists(
        helpers.ints(min_value=1, max_value=10), min_size=1, max_size=2
    ),
    dtype=helpers.get_dtypes("valid", full=False),
    num_positional_args=helpers.num_positional_args(fn_name="eye"),
)
def test_eye(
    *,
    n_rows,
    n_cols,
    k,
    batch_shape,
    dtype,
    device,
    as_variable,
    with_out,
    num_positional_args,
    fw,
):
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="eye",
        n_rows=n_rows,
        n_cols=n_cols,
        k=k,
        batch_shape=batch_shape,
        dtype=dtype,
        device=device,
    )


# from_dlpack
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="from_dlpack"),
)
def test_from_dlpack(
    *,
    dtype_and_x,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],  # can't convert variables
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="from_dlpack",
        x=x[0],
    )


@st.composite
def _fill_value(draw):
    dtype = draw(helpers.get_dtypes("numeric", full=False, key="dtype"))[0]
    if ivy.is_uint_dtype(dtype):
        return draw(helpers.ints(min_value=0, max_value=5))
    if ivy.is_int_dtype(dtype):
        return draw(helpers.ints(min_value=-5, max_value=5))
    return draw(helpers.floats(min_value=-5, max_value=5))


# full
@handle_cmd_line_args
@given(
    shape=helpers.get_shape(
        allow_none=False,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    fill_value=_fill_value(),
    dtypes=helpers.get_dtypes("numeric", full=False, key="dtype"),
    num_positional_args=helpers.num_positional_args(fn_name="full"),
)
def test_full(
    *,
    shape,
    fill_value,
    dtypes,
    with_out,
    device,
    num_positional_args,
    fw,
):
    helpers.test_function(
        input_dtypes=dtypes,
        as_variable_flags=[False],
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="full",
        shape=shape,
        fill_value=fill_value,
        dtype=dtypes[0],
        device=device,
    )


@st.composite
def _dtype_and_values(draw):
    return draw(
        helpers.dtype_and_values(
            min_num_dims=1,
            max_num_dims=5,
            min_dim_size=1,
            max_dim_size=5,
            dtype=draw(helpers.get_dtypes("numeric", full=False, key="dtype")),
        )
    )


# full_like
@handle_cmd_line_args
@given(
    dtype_and_x=_dtype_and_values(),
    fill_value=_fill_value(),
    num_positional_args=helpers.num_positional_args(fn_name="full_like"),
)
def test_full_like(
    *,
    dtype_and_x,
    device,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
    fill_value,
):
    dtype, x = dtype_and_x
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="full_like",
        x=x[0],
        fill_value=fill_value,
        dtype=dtype[0],
        device=device,
    )


# meshgrid
@handle_cmd_line_args
@given(
    dtype_and_arrays=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=st.integers(min_value=2, max_value=5),
        min_num_dims=1,
        max_num_dims=1,
        shared_dtype=True,
    ),
    sparse=st.booleans(),
    indexing=st.sampled_from(["xy", "ij"]),
)
def test_meshgrid(
    *,
    dtype_and_arrays,
    sparse,
    indexing,
    fw,
):
    dtype, arrays = dtype_and_arrays
    kw = {}
    i = 0
    for x_ in arrays:
        kw["x{}".format(i)] = x_
        i += 1

    num_positional_args = len(arrays)

    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="meshgrid",
        **kw,
        sparse=sparse,
        indexing=indexing,
    )


# ones
@handle_cmd_line_args
@given(
    shape=helpers.get_shape(
        allow_none=False,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    dtype=helpers.get_dtypes("numeric", full=False),
    num_positional_args=helpers.num_positional_args(fn_name="ones"),
)
def test_ones(
    *,
    shape,
    dtype,
    with_out,
    device,
    num_positional_args,
    fw,
):
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="ones",
        shape=shape,
        dtype=dtype,
        device=device,
    )


# ones_like
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="ones_like"),
)
def test_ones_like(
    *,
    dtype_and_x,
    device,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="ones_like",
        x=x[0],
        dtype=dtype,
        device=device,
    )


# tril
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=2,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    k=helpers.ints(min_value=-10, max_value=10),
    num_positional_args=helpers.num_positional_args(fn_name="tril"),
)
def test_tril(
    *,
    dtype_and_x,
    k,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x

    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="tril",
        x=x[0],
        k=k,
    )


# triu
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=2,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    k=helpers.ints(min_value=-10, max_value=10),
    num_positional_args=helpers.num_positional_args(fn_name="triu"),
)
def test_triu(
    *,
    dtype_and_x,
    k,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x

    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="triu",
        x=x[0],
        k=k,
    )


# zeros
@handle_cmd_line_args
@given(
    shape=helpers.get_shape(
        allow_none=False,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    dtype=helpers.get_dtypes("integer", full=False),
    num_positional_args=helpers.num_positional_args(fn_name="zeros"),
)
def test_zeros(
    *,
    shape,
    dtype,
    device,
    with_out,
    num_positional_args,
    fw,
):
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=[False],
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=[False],
        container_flags=[False],
        instance_method=False,
        fw=fw,
        fn_name="zeros",
        shape=shape,
        dtype=dtype,
        device=device,
    )


# zeros_like
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="zeros_like"),
)
def test_zeros_like(
    *,
    dtype_and_x,
    device,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    instance_method,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=[False],
        instance_method=instance_method,
        fw=fw,
        fn_name="zeros_like",
        x=x[0],
        dtype=dtype,
        device=device,
    )


# copy array
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(available_dtypes=helpers.get_dtypes("valid"))
)
def test_copy_array(dtype_and_x, device, fw):
    dtype, x = dtype_and_x
    # smoke test
    x = ivy.array(x[0], dtype=dtype[0], device=device)
    ret = ivy.copy_array(x)
    # type test
    assert ivy.is_ivy_array(ret)
    # cardinality test
    assert ret.shape == x.shape
    # value test
    helpers.assert_all_close(ivy.to_numpy(ret), ivy.to_numpy(x))
    assert id(x) != id(ret)


@st.composite
def _dtype_indices_depth_axis(draw):
    depth = draw(helpers.ints(min_value=2, max_value=100))
    dtype, indices, shape = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("numeric"),
            min_value=0,
            max_value=depth - 1,
            small_abs_safety_factor=4,
            ret_shape=True,
        )
    )

    axis = draw(st.integers(min_value=-1, max_value=len(shape) - 1))
    return dtype, indices, depth, axis


@st.composite
def _on_off_dtype(draw):
    dtype, value = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("numeric"), shape=(2,)
        )
    )
    [on_value, off_value] = value[0]
    return on_value, off_value, dtype[0]


# one_hot
@handle_cmd_line_args
@given(
    dtype_indices_depth_axis=_dtype_indices_depth_axis(),
    on_off_dtype=_on_off_dtype(),
    num_positional_args=helpers.num_positional_args(fn_name="one_hot"),
)
def test_one_hot(
    dtype_indices_depth_axis,
    on_off_dtype,
    with_out,
    as_variable,
    num_positional_args,
    native_array,
    container,
    instance_method,
    device,
    fw,
):
    input_dtype, indices, depth, axis = dtype_indices_depth_axis
    on_value, off_value, dtype = on_off_dtype

    helpers.test_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=fw,
        fn_name="one_hot",
        indices=indices[0],
        depth=depth,
        on_value=on_value,
        off_value=off_value,
        axis=axis,
        dtype=dtype,
    )
