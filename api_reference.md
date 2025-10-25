# Complex Type Expressions

These APIs are available on arrays, maps and structs.

## `ArrayValue`

### Methods

#### `length`

`length() -> ir.IntegerValue`

Compute the length of an array.

Returns
-------
IntegerValue
    The integer length of `self`

Examples
--------
>>> import ibis
>>> a = ibis.array([1, 2, 3])
>>> a.length()
ArrayLength((1, 2, 3))

#### `unnest`

`unnest() -> ir.Value`

Unnest an array.

Returns
-------
ir.Value
    Unnested array

---

## `StructValue`

### Methods

#### `destructure`

`destructure() -> DestructValue`

Destructure `self` into a `DestructValue`.

When assigned, a destruct value will be destructured and assigned to
multiple columns.

Returns
-------
DestructValue
    A destruct value expression.

#### `lift`

`lift() -> ir.Table`

Project the fields of `self` into a table.

This method is useful when analyzing data that has deeply nested
structs or arrays of structs. `lift` can be chained to avoid repeating
column names and table references.

See also [`Table.unpack`][ibis.expr.types.relations.Table.unpack].

Returns
-------
Table
    A projection with this struct expression's fields.

Examples
--------
>>> schema = dict(a="struct<b: float, c: string>", d="string")
>>> t = ibis.table(schema, name="t")
>>> t
UnboundTable: t
  a struct<b: float64, c: string>
  d string
>>> t.a.lift()
r0 := UnboundTable: t
  a struct<b: float64, c: string>
  d string

Selection[r0]
  selections:
    b: StructField(r0.a, field='b')
    c: StructField(r0.a, field='c')

---

## `MapValue`

### Methods

#### `get`

`get(key: ir.Value, default: ir.Value | None = None) -> ir.Value`

Return the value for `key` from `expr` or the default if `key` is not in the map.

Parameters
----------
key
    Expression to use for key
default
    Expression to return if `key` is not a key in `expr`

Returns
-------
Value
    The element type of `self`

Examples
--------
>>> import ibis
>>> m = ibis.map({"a": 1, "b": 2})
>>> m.get("a")
MapValueOrDefaultForKey(frozendict({'a': 1, 'b': 2}), key='a', default=None)
>>> m.get("c", 3)
MapValueOrDefaultForKey(frozendict({'a': 1, 'b': 2}), key='c', default=3)
>>> m.get("d")
MapValueOrDefaultForKey(frozendict({'a': 1, 'b': 2}), key='d', default=None)

#### `keys`

`keys() -> ir.ArrayValue`

Extract the keys of a map.

Returns
-------
ArrayValue
    The keys of `self`

Examples
--------
>>> import ibis
>>> m = ibis.map({"a": 1, "b": 2})
>>> m.keys()
MapKeys(frozendict({'a': 1, 'b': 2}))

#### `length`

`length() -> ir.IntegerValue`

Return the number of key-value pairs in the map.

Returns
-------
IntegerValue
    The number of elements in `self`

Examples
--------
>>> import ibis
>>> m = ibis.map({"a": 1, "b": 2})
>>> m.length()
MapLength(frozendict({'a': 1, 'b': 2}))

#### `values`

`values() -> ir.ArrayValue`

Extract the values of a map.

Returns
-------
ArrayValue
    The values of `self`

Examples
--------
>>> import ibis
>>> m = ibis.map({"a": 1, "b": 2})
>>> m.keys()
MapKeys(frozendict({'a': 1, 'b': 2}))

---



# Generic Expression APIs

These expressions are available on scalars and columns of any element type.

## `Value`

### Methods

#### `between`

`between(lower: Value, upper: Value) -> ir.BooleanValue`

Check if this expression is between `lower` and `upper`, inclusive.

Parameters
----------
lower
    Lower bound
upper
    Upper bound

Returns
-------
BooleanValue
    Expression indicating membership in the provided range

#### `case`

`case()`

Create a SimpleCaseBuilder to chain multiple if-else statements.

Add new search expressions with the `.when()` method. These must be
comparable with this column expression. Conclude by calling `.end()`

Returns
-------
SimpleCaseBuilder
    A case builder

Examples
--------
>>> import ibis
>>> t = ibis.table([('string_col', 'string')], name='t')
>>> expr = t.string_col
>>> case_expr = (expr.case()
...              .when('a', 'an a')
...              .when('b', 'a b')
...              .else_('null or (not a and not b)')
...              .end())
>>> case_expr
r0 := UnboundTable[t]
  string_col string
SimpleCase(base=r0.string_col, cases=[ValueList(values=['a', 'b'])], results=[ValueList(values=['an a', 'a b'])], default='null or (not a and not b)')

#### `cases`

`cases(case_result_pairs: Iterable[tuple[ir.BooleanValue, Value]], default: Value | None = None) -> Value`

Create a case expression in one shot.

Parameters
----------
case_result_pairs
    Conditional-result pairs
default
    Value to return if none of the case conditions are true

Returns
-------
Value
    Value expression

#### `cast`

`cast(target_type: dt.DataType) -> Value`

Cast expression to indicated data type.

Parameters
----------
target_type
    Type to cast to

Returns
-------
Value
    Casted expression

#### `coalesce`

`coalesce(*args: Value) -> Value`

Return the first non-null value from `args`.

Parameters
----------
args
    Arguments from which to choose the first non-null value

Returns
-------
Value
    Coalesced expression

Examples
--------
>>> import ibis
>>> ibis.coalesce(None, 4, 5)
Coalesce([ValueList(values=[None, 4, 5])])

#### `collect`

`collect() -> ir.ArrayValue`

Return an array of the elements of this expression.

#### `fillna`

`fillna(fill_value: Scalar) -> Value`

Replace any null values with the indicated fill value.

Parameters
----------
fill_value
    Value with which to replace `NA` values in `self`

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(col='int64', other_col='int64'))
>>> result = table.col.fillna(5)
r0 := UnboundTable: unbound_table_0
  col       int64
  other_col int64
IfNull(r0.col, ifnull_expr=5)
>>> table.col.fillna(table.other_col * 3)
r0 := UnboundTable: unbound_table_0
  col       int64
  other_col int64
IfNull(r0.col, ifnull_expr=r0.other_col * 3)

Returns
-------
Value
    `self` filled with `fill_value` where it is `NA`

#### `greatest`

`greatest(*args: ir.Value) -> ir.Value`

Compute the largest value among the supplied arguments.

Parameters
----------
args
    Arguments to choose from

Returns
-------
Value
    Maximum of the passed arguments

#### `group_concat`

`group_concat(sep: str = ',', where: ir.BooleanValue | None = None) -> ir.StringScalar`

Concatenate values using the indicated separator to produce a
string.

Parameters
----------
sep
    Separator will be used to join strings
where
    Filter expression

Returns
-------
StringScalar
    Concatenated string expression

#### `hash`

`hash(how: str = 'fnv') -> ir.IntegerValue`

Compute an integer hash value.

Parameters
----------
how
    Hash algorithm to use

Returns
-------
IntegerValue
    The hash value of `self`

#### `identical_to`

`identical_to(other: Value) -> ir.BooleanValue`

Return whether this expression is identical to other.

Corresponds to `IS NOT DISTINCT FROM` in SQL.

Parameters
----------
other
    Expression to compare to

Returns
-------
BooleanValue
    Whether this expression is not distinct from `other`

#### `isin`

`isin(values: Value | Sequence[Value]) -> ir.BooleanValue`

Check whether this expression's values are in `values`.

Parameters
----------
values
    Values or expression to check for membership

Returns
-------
BooleanValue
    Expression indicating membership

Examples
--------
Check whether a column's values are contained in a sequence

>>> import ibis
>>> table = ibis.table(dict(string_col='string'))
>>> table.string_col.isin(['foo', 'bar', 'baz'])
r0 := UnboundTable: unbound_table_1
  string_col string
Contains(value=r0.string_col, options=[ValueList(values=['foo', 'bar', 'baz'])])

Check whether a column's values are contained in another table's column

>>> table2 = ibis.table(dict(other_string_col='string'))
>>> table.string_col.isin(table2.other_string_col)
r0 := UnboundTable: unbound_table_3
  other_string_col string
r1 := UnboundTable: unbound_table_1
  string_col string
Contains(value=r1.string_col, options=r0.other_string_col)

#### `isnull`

`isnull() -> ir.BooleanValue`

Return whether this expression is NULL.

#### `least`

`least(*args: ir.Value) -> ir.Value`

Compute the smallest value among the supplied arguments.

Parameters
----------
args
    Arguments to choose from

Returns
-------
Value
    Minimum of the passed arguments

#### `name`

`name(name)`

Rename an expression to `name`.

Parameters
----------
name
    The new name of the expression

Returns
-------
Value
    `self` with name `name`

Examples
--------
>>> import ibis
>>> t = ibis.table(dict(a="int64"))
>>> t.a.name("b")
r0 := UnboundTable[unbound_table_...]
  a int64
b: r0.a

#### `notin`

`notin(values: Value | Sequence[Value]) -> ir.BooleanValue`

Check whether this expression's values are not in `values`.

Parameters
----------
values
    Values or expression to check for lack of membership

Returns
-------
BooleanValue
    Whether `self`'s values are not contained in `values`

#### `notnull`

`notnull() -> ir.BooleanValue`

Return whether this expression is not NULL.

#### `nullif`

`nullif(null_if_expr: Value) -> Value`

Set values to null if they equal the values `null_if_expr`.

Commonly use to avoid divide-by-zero problems by replacing zero with
`NULL` in the divisor.

Parameters
----------
null_if_expr
    Expression indicating what values should be NULL

Returns
-------
Value
    Value expression

#### `over`

`over(window: win.Window) -> Value`

Construct a window expression.

Parameters
----------
window
    Window specification

Returns
-------
Value
    A window function expression

#### `substitute`

`substitute(value: Value, replacement: Value | None = None, else_: Value | None = None)`

Replace one or more values in a value expression.

Parameters
----------
value
    Expression or mapping
replacement
    Expression. If an expression is passed to value, this must be
    passed.
else_
    Expression

Returns
-------
Value
    Replaced values

#### `type`

`type()`

#### `typeof`

`typeof() -> ir.StringValue`

Return the data type of the expression.

The values of the returned strings are necessarily backend dependent.

Returns
-------
StringValue
    A string indicating the type of the value

---

## `Column`

### Methods

#### `approx_median`

`approx_median(where: ir.BooleanValue | None = None) -> Scalar`

Return an approximate of the median of `self`.

!!! info "The result may or may not be exact"

    Whether the result is an approximation depends on the backend.

    !!! warning "Do not depend on the results being exact"

Parameters
----------
where
    Filter in values when `where` is `True`

Returns
-------
Scalar
    An approximation of the median of `self`

#### `approx_nunique`

`approx_nunique(where: ir.BooleanValue | None = None) -> ir.IntegerScalar`

Return the approximate number of distinct elements in `self`.

!!! info "The result may or may not be exact"

    Whether the result is an approximation depends on the backend.

    !!! warning "Do not depend on the results being exact"

Parameters
----------
where
    Filter in values when `where` is `True`

Returns
-------
Scalar
    An approximate count of the distinct elements of `self`

#### `arbitrary`

`arbitrary(where: ir.BooleanValue | None = None, how: Literal['first', 'last', 'heavy'] | None = None) -> Scalar`

Select an arbitrary value in a column.

Parameters
----------
where
    A filter expression
how
    The method to use for selecting the element.

    * `"first"`: Select the first non-`NULL` element
    * `"last"`: Select the last non-`NULL` element
    * `"heavy"`: Select a frequently occurring value using the heavy
      hitters algorithm. `"heavy"` is only supported by Clickhouse
      backend.

Returns
-------
Scalar
    An expression

#### `argmax`

`argmax(key: ir.Value, where: ir.BooleanValue | None = None) -> Scalar`

Return the value of `self` that maximizes `key`.

#### `argmin`

`argmin(key: ir.Value, where: ir.BooleanValue | None = None) -> Scalar`

Return the value of `self` that minimizes `key`.

#### `bottomk`

`bottomk(k: int, by: Value | None = None) -> ir.TopK`

#### `count`

`count(where: ir.BooleanValue | None = None) -> ir.IntegerScalar`

Compute the number of rows in an expression.

Parameters
----------
where
    Filter expression

Returns
-------
IntegerScalar
    Number of elements in an expression

#### `cume_dist`

`cume_dist() -> Column`

#### `cummax`

`cummax() -> Column`

#### `cummin`

`cummin() -> Column`

#### `dense_rank`

`dense_rank() -> Column`

#### `first`

`first() -> Column`

#### `lag`

`lag(offset: int | ir.IntegerValue | None = None, default: Value | None = None) -> Column`

#### `last`

`last() -> Column`

#### `lead`

`lead(offset: int | ir.IntegerValue | None = None, default: Value | None = None) -> Column`

#### `max`

`max(where: ir.BooleanValue | None = None) -> Scalar`

Return the maximum of a column.

#### `min`

`min(where: ir.BooleanValue | None = None) -> Scalar`

Return the minimum of a column.

#### `nth`

`nth(n: int | ir.IntegerValue) -> Column`

Return the `n`th value over a window.

Parameters
----------
n
    Desired rank value

Returns
-------
Column
    The nth value over a window

#### `ntile`

`ntile(buckets: int | ir.IntegerValue) -> ir.IntegerColumn`

#### `nunique`

`nunique(where: ir.BooleanValue | None = None) -> ir.IntegerScalar`

#### `parent`

`parent()`

#### `percent_rank`

`percent_rank() -> Column`

#### `rank`

`rank() -> Column`

#### `summary`

`summary(exact_nunique: bool = False, prefix: str = '', suffix: str = '') -> list[ir.NumericScalar]`

Compute a set of summary metrics.

Parameters
----------
exact_nunique
    Compute the exact number of distinct values. Typically slower if
    `True`.
prefix
    String prefix for metric names
suffix
    String suffix for metric names

Returns
-------
list[NumericScalar]
    Metrics list

#### `to_projection`

`to_projection() -> ir.Table`

Promote this column expression to a projection.

#### `topk`

`topk(k: int, by: ir.Value | None = None) -> ir.TopK`

Return a "top k" expression.

Parameters
----------
k
    Return this number of rows
by
    An expression. Defaults to the count

Returns
-------
TopK
    A top-k expression

#### `value_counts`

`value_counts(metric_name: str = 'count') -> ir.Table`

Compute a frequency table.

Returns
-------
Table
    Frequency table expression

---

## `Scalar`

### Methods

#### `to_projection`

`to_projection() -> ir.Table`

Promote this scalar expression to a projection.

---



# Geospatial Expressions

Ibis supports the following geospatial expression APIs

## `GeoSpatialValue`

### Methods

#### `area`

`area() -> ir.FloatingValue`

Compute the area of a geospatial value.

Returns
-------
FloatingValue
    The area of `self`

#### `as_binary`

`as_binary() -> ir.BinaryValue`

Get the geometry as well-known bytes (WKB) without the SRID data.

Returns
-------
BinaryValue
    Binary value

#### `as_ewkb`

`as_ewkb() -> ir.BinaryValue`

Get the geometry as well-known bytes (WKB) with the SRID data.

Returns
-------
BinaryValue
    WKB value

#### `as_ewkt`

`as_ewkt() -> ir.StringValue`

Get the geometry as well-known text (WKT) with the SRID data.

Returns
-------
StringValue
    String value

#### `as_text`

`as_text() -> ir.StringValue`

Get the geometry as well-known text (WKT) without the SRID data.

Returns
-------
StringValue
    String value

#### `azimuth`

`azimuth(right: GeoSpatialValue) -> ir.FloatingValue`

Return the angle in radians from the horizontal of the vector
defined by `self` and `right`.

Angle is computed clockwise from down-to-up on the clock:
12=0; 3=PI/2; 6=PI; 9=3PI/2.

Parameters
----------
right
    Right geometry

Returns
-------
FloatingValue
    azimuth

#### `buffer`

`buffer(radius: float | ir.FloatingValue) -> GeoSpatialValue`

Returns a geometry that represents all points whose distance from
this Geometry is less than or equal to distance. Calculations are in
the Spatial Reference System of this Geometry.

Parameters
----------
radius
    Floating expression

Returns
-------
GeoSpatialValue
    Geometry expression

#### `centroid`

`centroid() -> PointValue`

Returns the centroid of the geometry.

Returns
-------
PointValue
    The centroid

#### `contains`

`contains(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometry contains the `right`.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` contains `right`

#### `contains_properly`

`contains_properly(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the first geometry contains the second one.

Excludes common border points.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether self contains right excluding border points.

#### `covered_by`

`covered_by(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the first geometry is covered by the second one.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` is covered by `right`

#### `covers`

`covers(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the first geometry covers the second one.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` covers `right`

#### `crosses`

`crosses(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometries have at least one interior point in common.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` and `right` have at least one common interior point.

#### `d_fully_within`

`d_fully_within(right: GeoSpatialValue, distance: ir.FloatingValue) -> ir.BooleanValue`

Check if `self` is entirely within `distance` from `right`.

Parameters
----------
right
    Right geometry
distance
    Distance to check

Returns
-------
BooleanValue
    Whether `self` is within a specified distance from `right`.

#### `d_within`

`d_within(right: GeoSpatialValue, distance: ir.FloatingValue) -> ir.BooleanValue`

Check if `self` is partially within `distance` from `right`.

Parameters
----------
right
    Right geometry
distance
    Distance to check

Returns
-------
BooleanValue
    Whether `self` is partially within `distance` from `right`.

#### `difference`

`difference(right: GeoSpatialValue) -> GeoSpatialValue`

Return the difference of two geometries.

Parameters
----------
right
    Right geometry

Returns
-------
GeoSpatialValue
    Difference of `self` and `right`

#### `disjoint`

`disjoint(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometries have no points in common.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` and `right` are disjoint

#### `distance`

`distance(right: GeoSpatialValue) -> ir.FloatingValue`

Compute the distance between two geospatial expressions.

Parameters
----------
right
    Right geometry or geography

Returns
-------
FloatingValue
    Distance between `self` and `right`

#### `end_point`

`end_point() -> PointValue`

Return the last point of a `LINESTRING` geometry as a `POINT`.

Return `NULL` if the input parameter is not a `LINESTRING`

Returns
-------
PointValue
    End point

#### `envelope`

`envelope() -> ir.PolygonValue`

Returns a geometry representing the bounding box of `self`.

Returns
-------
PolygonValue
    A polygon

#### `geo_equals`

`geo_equals(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometries are equal.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` equals `right`

#### `geometry_n`

`geometry_n(n: int | ir.IntegerValue) -> GeoSpatialValue`

Get the 1-based Nth geometry of a multi geometry.

Parameters
----------
n
    Nth geometry index

Returns
-------
GeoSpatialValue
    Geometry value

#### `geometry_type`

`geometry_type() -> ir.StringValue`

Get the type of a geometry.

Returns
-------
StringValue
    String representing the type of `self`.

#### `intersection`

`intersection(right: GeoSpatialValue) -> GeoSpatialValue`

Return the intersection of two geometries.

Parameters
----------
right
    Right geometry

Returns
-------
GeoSpatialValue
    Intersection of `self` and `right`

#### `intersects`

`intersects(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometries share any points.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` intersects `right`

#### `is_valid`

`is_valid() -> ir.BooleanValue`

Check if the geometry is valid.

Returns
-------
BooleanValue
    Whether `self` is valid

#### `length`

`length() -> ir.FloatingValue`

Compute the length of a geospatial expression.

Returns
-------
FloatingValue
    Length of `self`

#### `line_locate_point`

`line_locate_point(right: PointValue) -> ir.FloatingValue`

Locate the distance a point falls along the length of a line.

Returns a float between zero and one representing the location of the
closest point on the linestring to the given point, as a fraction of
the total 2d line length.

Parameters
----------
right
    Point geometry

Returns
-------
FloatingValue
    Fraction of the total line length

#### `line_merge`

`line_merge() -> ir.LineStringValue`

Merge a `MultiLineString` into a `LineString`.

Returns a (set of) LineString(s) formed by sewing together the
constituent line work of a MultiLineString. If a geometry other than
a LineString or MultiLineString is given, this will return an empty
geometry collection.

Returns
-------
GeoSpatialValue
    Merged linestrings

#### `line_substring`

`line_substring(start: ir.FloatingValue, end: ir.FloatingValue) -> ir.LineStringValue`

Clip a substring from a LineString.

Returns a linestring that is a substring of the input one, starting
and ending at the given fractions of the total 2d length. The second
and third arguments are floating point values between zero and one.
This only works with linestrings.

Parameters
----------
start
    Start value
end
    End value

Returns
-------
LineStringValue
    Clipped linestring

#### `max_distance`

`max_distance(right: GeoSpatialValue) -> ir.FloatingValue`

Returns the 2-dimensional maximum distance between two geometries in
projected units.

If `self` and `right` are the same geometry the function will return
the distance between the two vertices most far from each other in that
geometry.

Parameters
----------
right
    Right geometry

Returns
-------
FloatingValue
    Maximum distance

#### `n_points`

`n_points() -> ir.IntegerValue`

Return the number of points in a geometry. Works for all geometries

Returns
-------
IntegerValue
    Number of points

#### `n_rings`

`n_rings() -> ir.IntegerValue`

Return the number of rings for polygons and multipolygons.

Outer rings are counted as well.

Returns
-------
IntegerValue
    Number of rings

#### `ordering_equals`

`ordering_equals(right: GeoSpatialValue) -> ir.BooleanValue`

Check if two geometries are equal and have the same point ordering.

Returns true if the two geometries are equal and the coordinates
are in the same order.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether points and orderings are equal.

#### `overlaps`

`overlaps(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometries share space, have the same dimension, and
are not completely contained by each other.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Overlaps indicator

#### `perimeter`

`perimeter() -> ir.FloatingValue`

Compute the perimeter of a geospatial expression.

Returns
-------
FloatingValue
    Perimeter of `self`

#### `point_n`

`point_n(n: ir.IntegerValue) -> PointValue`

Return the Nth point in a single linestring in the geometry.
Negative values are counted backwards from the end of the LineString,
so that -1 is the last point. Returns NULL if there is no linestring in
the geometry

Parameters
----------
n
    Nth point index

Returns
-------
PointValue
    Nth point in `self`

#### `set_srid`

`set_srid(srid: ir.IntegerValue) -> GeoSpatialValue`

Set the spatial reference identifier for the `ST_Geometry`.

Parameters
----------
srid
    SRID integer value

Returns
-------
GeoSpatialValue
    `self` with SRID set to `srid`

#### `simplify`

`simplify(tolerance: ir.FloatingValue, preserve_collapsed: ir.BooleanValue) -> GeoSpatialValue`

Simplify a given geometry.

Parameters
----------
tolerance
    Tolerance
preserve_collapsed
    Whether to preserve collapsed geometries

Returns
-------
GeoSpatialValue
    Simplified geometry

#### `srid`

`srid() -> ir.IntegerValue`

Return the spatial reference identifier for the ST_Geometry.

Returns
-------
IntegerValue
    SRID

#### `start_point`

`start_point() -> PointValue`

Return the first point of a `LINESTRING` geometry as a `POINT`.

Return `NULL` if the input parameter is not a `LINESTRING`

Returns
-------
PointValue
    Start point

#### `touches`

`touches(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the geometries have at least one point in common, but do
not intersect.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether self and right are touching

#### `transform`

`transform(srid: ir.IntegerValue) -> GeoSpatialValue`

Transform a geometry into a new SRID.

Parameters
----------
srid
    Integer expression

Returns
-------
GeoSpatialValue
    Transformed geometry

#### `union`

`union(right: GeoSpatialValue) -> GeoSpatialValue`

Merge two geometries into a union geometry.

Returns the pointwise union of the two geometries.
This corresponds to the non-aggregate version the PostGIS ST_Union.

Parameters
----------
right
    Right geometry

Returns
-------
GeoSpatialValue
    Union of geometries

#### `within`

`within(right: GeoSpatialValue) -> ir.BooleanValue`

Check if the first geometry is completely inside of the second.

Parameters
----------
right
    Right geometry

Returns
-------
BooleanValue
    Whether `self` is in `right`.

#### `x`

`x() -> ir.FloatingValue`

Return the X coordinate of `self`, or NULL if not available.

Input must be a point.

Returns
-------
FloatingValue
    X coordinate of `self`

#### `x_max`

`x_max() -> ir.FloatingValue`

Return the X maxima of a geometry.

Returns
-------
FloatingValue
    X maxima

#### `x_min`

`x_min() -> ir.FloatingValue`

Return the X minima of a geometry.

Returns
-------
FloatingValue
    X minima

#### `y`

`y() -> ir.FloatingValue`

Return the Y coordinate of `self`, or NULL if not available.

Input must be a point.

Returns
-------
FloatingValue
    Y coordinate of `self`

#### `y_max`

`y_max() -> ir.FloatingValue`

Return the Y maxima of a geometry.

Returns
-------
FloatingValue
    Y maxima

#### `y_min`

`y_min() -> ir.FloatingValue`

Return the Y minima of a geometry.

Returns
-------
FloatingValue
    Y minima

---

## `GeoSpatialColumn`

### Methods

#### `unary_union`

`unary_union() -> ir.GeoSpatialScalar`

Aggregate a set of geometries into a union.

This corresponds to the aggregate version of the PostGIS ST_Union.
We give it a different name (following the corresponding method
in GeoPandas) to avoid name conflicts with the non-aggregate version.

Returns
-------
GeoSpatialScalar
    Union of geometries

---



# Base Expression Types

These APIs are shared by both table and column expressions.

## `Expr`

### Methods

#### `compile`

`compile(limit: int | None = None, timecontext: TimeContext | None = None, params: Mapping[Value, Any] | None = None)`

Compile to an execution target.

Parameters
----------
limit
    An integer to effect a specific row limit. A value of `None` means
    "no limit". The default is in `ibis/config.py`.
timecontext
    Defines a time range of `(begin, end)`. When defined, the execution
    will only compute result for data inside the time range. The time
    range is inclusive of both endpoints. This is conceptually same as
    a time filter.
    The time column must be named `'time'` and should preserve
    across the expression. For example, if that column is dropped then
    execute will result in an error.
params
    Mapping of scalar parameter expressions to value

#### `equals`

`equals(other)`

#### `execute`

`execute(limit: int | str | None = 'default', timecontext: TimeContext | None = None, params: Mapping[Value, Any] | None = None, **kwargs: Any)`

Execute an expression against its backend if one exists.

Parameters
----------
limit
    An integer to effect a specific row limit. A value of `None` means
    "no limit". The default is in `ibis/config.py`.
timecontext
    Defines a time range of `(begin, end)`. When defined, the execution
    will only compute result for data inside the time range. The time
    range is inclusive of both endpoints. This is conceptually same as
    a time filter.
    The time column must be named `'time'` and should preserve
    across the expression. For example, if that column is dropped then
    execute will result in an error.
params
    Mapping of scalar parameter expressions to value

#### `get_name`

`get_name()`

#### `has_name`

`has_name()`

#### `op`

`op() -> ops.Node`

#### `pipe`

`pipe(f, *args: Any, **kwargs: Any) -> Expr`

Compose `f` with `self`.

Parameters
----------
f
    If the expression needs to be passed as anything other than the
    first argument to the function, pass a tuple with the argument
    name. For example, (f, 'data') if the function f expects a 'data'
    keyword
args
    Positional arguments to `f`
kwargs
    Keyword arguments to `f`

Examples
--------
>>> import ibis
>>> t = ibis.table([('a', 'int64'), ('b', 'string')], name='t')
>>> f = lambda a: (a + 1).name('a')
>>> g = lambda a: (a * 2).name('a')
>>> result1 = t.a.pipe(f).pipe(g)
>>> result1
r0 := UnboundTable[t]
  a int64
  b string
a: r0.a + 1 * 2

>>> result2 = g(f(t.a))  # equivalent to the above
>>> result1.equals(result2)
True

Returns
-------
Expr
    Result type of passed function

#### `verify`

`verify()`

Return True if expression can be compiled to its attached client.

#### `visualize`

`visualize(format: str = 'svg') -> None`

Visualize an expression in the browser as an SVG image.

Parameters
----------
format
    Image output format. These are specified by the ``graphviz`` Python
    library.

Notes
-----
This method opens a web browser tab showing the image of the expression
graph created by the code in [ibis.expr.visualize][].

Raises
------
ImportError
    If ``graphviz`` is not installed.

---



# Numeric and Boolean Expressions

These APIs are available on numeric and boolean expressions.

## `NumericValue`

### Methods

#### `abs`

`abs() -> NumericValue`

Return the absolute value of `self`.

#### `acos`

`acos() -> NumericValue`

Compute the arc cosine of `self`.

#### `asin`

`asin() -> NumericValue`

Compute the arc sine of `self`.

#### `atan`

`atan() -> NumericValue`

Compute the arc tangent of `self`.

#### `atan2`

`atan2(other: NumericValue) -> NumericValue`

Compute the two-argument version of arc tangent.

#### `ceil`

`ceil() -> DecimalValue | IntegerValue`

Return the ceiling of `self`.

#### `clip`

`clip(lower: NumericValue | None = None, upper: NumericValue | None = None) -> NumericValue`

Trim values outside of `lower` and `upper` bounds.

Parameters
----------
lower
    Lower bound
upper
    Upper bound

Returns
-------
NumericValue
    Clipped input

#### `cos`

`cos() -> NumericValue`

Compute the cosine of `self`.

#### `cot`

`cot() -> NumericValue`

Compute the cotangent of `self`.

#### `degrees`

`degrees() -> NumericValue`

Compute the degrees of `self` radians.

#### `exp`

`exp() -> NumericValue`

Compute $e^\texttt{self}$.

Returns
-------
NumericValue
    $e^\texttt{self}$

#### `floor`

`floor() -> DecimalValue | IntegerValue`

Return the floor of an expression.

#### `ln`

`ln() -> NumericValue`

Compute $\ln\left(\texttt{self}\right)$.

#### `log`

`log(base: NumericValue | None = None) -> NumericValue`

Return the logarithm using a specified base.

Parameters
----------
base
    The base of the logarithm. If `None`, base `e` is used.

Returns
-------
NumericValue
    Logarithm of `arg` with base `base`

#### `log10`

`log10() -> NumericValue`

Compute $\log_{10}\left(\texttt{self}\right)$.

#### `log2`

`log2() -> NumericValue`

Compute $\log_{2}\left(\texttt{self}\right)$.

#### `negate`

`negate() -> NumericValue`

Negate a numeric expression.

Returns
-------
NumericValue
    A numeric value expression

#### `nullifzero`

`nullifzero() -> NumericValue`

Return `NULL` if an expression is zero.

#### `point`

`point(right: int | float | NumericValue) -> ir.PointValue`

Return a point constructed from the coordinate values.

Constant coordinates result in construction of a `POINT` literal or
column.

Parameters
----------
right
    Y coordinate

Returns
-------
PointValue
    Points

#### `radians`

`radians() -> NumericValue`

Compute radians from `self` degrees.

#### `round`

`round(digits: int | IntegerValue | None = None) -> NumericValue`

Round values to an indicated number of decimal places.

Parameters
----------
digits
    The number of digits to round to.

    Here's how the `digits` parameter affects the expression output
    type:

    |   `digits`    | `self.type()` |  Output   |
    | :-----------: | :-----------: | :-------: |
    | `None` or `0` |   `decimal`   | `decimal` |
    |    Nonzero    |   `decimal`   | `decimal` |
    | `None` or `0` |   Floating    |  `int64`  |
    |    Nonzero    |   Floating    | `float64` |

Returns
-------
NumericValue
    The rounded expression

#### `sign`

`sign() -> NumericValue`

Return the sign of the input.

#### `sin`

`sin() -> NumericValue`

Compute the sine of `self`.

#### `sqrt`

`sqrt() -> NumericValue`

Compute the square root of `self`.

#### `tan`

`tan() -> NumericValue`

Compute the tangent of `self`.

#### `zeroifnull`

`zeroifnull() -> NumericValue`

Return zero if an expression is `NULL`.

---

## `NumericColumn`

### Methods

#### `bucket`

`bucket(buckets: Sequence[int], closed: Literal['left', 'right'] = 'left', close_extreme: bool = True, include_under: bool = False, include_over: bool = False) -> ir.CategoryColumn`

Compute a discrete binning of a numeric array.

Parameters
----------
buckets
    List of buckets
closed
    Which side of each interval is closed. For example:

    ```python
    buckets = [0, 100, 200]
    closed = "left"  # 100 falls in 2nd bucket
    closed = "right"  # 100 falls in 1st bucket
    ```
close_extreme
    Whether the extreme values fall in the last bucket
include_over
    Include values greater than the last bucket in the last bucket
include_under
    Include values less than the first bucket in the first bucket

Returns
-------
CategoryColumn
    A categorical column expression

#### `corr`

`corr(right: NumericColumn, where: ir.BooleanValue | None = None, how: Literal['sample', 'pop'] = 'sample') -> NumericScalar`

Return the correlation of two numeric columns.

Parameters
----------
right
    Numeric column
where
    Filter
how
    Population or sample correlation

Returns
-------
NumericScalar
    The correlation of `left` and `right`

#### `cov`

`cov(right: NumericColumn, where: ir.BooleanValue | None = None, how: Literal['sample', 'pop'] = 'sample') -> NumericScalar`

Return the covariance of two numeric columns.

Parameters
----------
right
    Numeric column
where
    Filter
how
    Population or sample covariance

Returns
-------
NumericScalar
    The covariance of `self` and `right`

#### `cummean`

`cummean() -> NumericColumn`

#### `cumsum`

`cumsum() -> NumericColumn`

#### `histogram`

`histogram(nbins: int | None = None, binwidth: float | None = None, base: float | None = None, closed: Literal['left', 'right'] = 'left', aux_hash: str | None = None) -> ir.CategoryColumn`

Compute a histogram with fixed width bins.

Parameters
----------
nbins
    If supplied, will be used to compute the binwidth
binwidth
    If not supplied, computed from the data (actual max and min values)
base
    Histogram base
closed
    Which side of each interval is closed
aux_hash
    Auxiliary hash value to add to bucket names

Returns
-------
CategoryColumn
    Coded value expression

#### `mean`

`mean(where: ir.BooleanValue | None = None) -> NumericScalar`

Return the mean of a numeric column.

Parameters
----------
where
    Filter

Returns
-------
NumericScalar
    The mean of the input expression

#### `quantile`

`quantile(quantile: Sequence[NumericValue | float], interpolation: Literal['linear', 'lower', 'higher', 'midpoint', 'nearest'] = 'linear') -> NumericScalar`

Return value at the given quantile.

Parameters
----------
quantile
    `0 <= quantile <= 1`, the quantile(s) to compute
interpolation
    This optional parameter specifies the interpolation method to use,
    when the desired quantile lies between two data points `i` and `j`:

    * linear: `i + (j - i) * fraction`, where `fraction` is the
      fractional part of the index surrounded by `i` and `j`.
    * lower: `i`.
    * higher: `j`.
    * nearest: `i` or `j` whichever is nearest.
    * midpoint: (`i` + `j`) / 2.

Returns
-------
NumericScalar
    Quantile of the input

#### `std`

`std(where: ir.BooleanValue | None = None, how: Literal['sample', 'pop'] = 'sample') -> NumericScalar`

Return the standard deviation of a numeric column.

Parameters
----------
where
    Filter
how
    Sample or population standard deviation

Returns
-------
NumericScalar
    Standard deviation of `arg`

#### `sum`

`sum(where: ir.BooleanValue | None = None) -> NumericScalar`

Return the sum of a numeric column.

Parameters
----------
where
    Filter

Returns
-------
NumericScalar
    The sum of the input expression

#### `summary`

`summary(exact_nunique: bool = False, prefix: str = '', suffix: str = '') -> list[NumericScalar]`

Compute a set of summary metrics from the input numeric value
expression.

Parameters
----------
exact_nunique
    Compute the exact number of distinct values. Typically slower if
    `True`.
prefix
    String prefix for metric names
suffix
    String suffix for metric names

Returns
-------
list[NumericScalar]
    Metrics list

#### `var`

`var(where: ir.BooleanValue | None = None, how: Literal['sample', 'pop'] = 'sample') -> NumericScalar`

Return the variance of a numeric column.

Parameters
----------
where
    Filter
how
    Sample or population variance

Returns
-------
NumericScalar
    Standard deviation of `arg`

---


## `IntegerValue`

### Methods

#### `convert_base`

`convert_base(from_base: IntegerValue, to_base: IntegerValue) -> IntegerValue`

Convert an integer from one base to another.

Parameters
----------
from_base
    Numeric base of expression
to_base
    New base

Returns
-------
IntegerValue
    Converted expression

#### `to_interval`

`to_interval(unit: Literal['Y', 'M', 'W', 'D', 'h', 'm', 's', 'ms', 'us', 'ns'] = 's') -> ir.IntervalValue`

Convert an integer to an interval.

Parameters
----------
unit
    Unit for the resulting interval

Returns
-------
IntervalValue
    An interval in units of `unit`

#### `to_timestamp`

`to_timestamp(unit: Literal['s', 'ms', 'us'] = 's') -> ir.TimestampValue`

Convert an integral UNIX timestamp to a timestamp expression.

Parameters
----------
unit
    The resolution of `arg`

Returns
-------
TimestampValue
    `self` converted to a timestamp

---

## `IntegerColumn`

### Methods

#### `bit_and`

`bit_and(where: ir.BooleanValue | None = None) -> IntegerScalar`

Aggregate the column using the bitwise and operator.

#### `bit_or`

`bit_or(where: ir.BooleanValue | None = None) -> IntegerScalar`

Aggregate the column using the bitwise or operator.

#### `bit_xor`

`bit_xor(where: ir.BooleanValue | None = None) -> IntegerScalar`

Aggregate the column using the bitwise exclusive or operator.

---


## `FloatingValue`

### Methods

#### `isinf`

`isinf() -> ir.BooleanValue`

Return whether the value is infinity.

#### `isnan`

`isnan() -> ir.BooleanValue`

Return whether the value is NaN.

---


## `DecimalValue`

### Methods

#### `precision`

`precision() -> IntegerValue`

Return the precision of `arg`.

Returns
-------
IntegerValue
    The precision of the expression.

#### `scale`

`scale() -> IntegerValue`

Return the scale of `arg`.

Returns
-------
IntegerValue
    The scale of the expression.

---


## `BooleanValue`

### Methods

#### `ifelse`

`ifelse(true_expr: ir.Value, false_expr: ir.Value) -> ir.Value`

Construct a ternary conditional expression.

Parameters
----------
true_expr
    Expression to return if `self` evaluates to `True`
false_expr
    Expression to return if `self` evaluates to `False`

Returns
-------
Value
    The value of `true_expr` if `arg` is `True` else `false_expr`

Examples
--------
>>> import ibis
>>> t = ibis.table([("is_person", "boolean")], name="t")
>>> expr = t.is_person.ifelse("yes", "no")
>>> print(ibis.impala.compile(expr))
SELECT CASE WHEN `is_person` THEN 'yes' ELSE 'no' END AS `tmp`
FROM t

---



# String Expressions

All string operations are valid for both scalars and columns.

## `StringValue`

### Methods

#### `ascii_str`

`ascii_str() -> ir.IntegerValue`

Return the numeric ASCII code of the first character of a string.

Returns
-------
IntegerValue
    ASCII code of the first character of the input

#### `capitalize`

`capitalize() -> StringValue`

Capitalize the input string.

Returns
-------
StringValue
    Capitalized string

#### `concat`

`concat(other: str | StringValue, *args: str | StringValue) -> StringValue`

Concatenate strings.

Parameters
----------
other
    String to concatenate
args
    Additional strings to concatenate

Returns
-------
StringValue
    All strings concatenated

#### `contains`

`contains(substr: str | StringValue) -> ir.BooleanValue`

Return whether the expression contains `substr`.

Parameters
----------
substr
    Substring for which to check

Returns
-------
BooleanValue
    Boolean indicating the presence of `substr` in the expression

#### `convert_base`

`convert_base(from_base: int | ir.IntegerValue, to_base: int | ir.IntegerValue) -> ir.IntegerValue`

Convert a string representing an integer from one base to another.

Parameters
----------
from_base
    Numeric base of the expression
to_base
    New base

Returns
-------
IntegerValue
    Converted expression

#### `endswith`

`endswith(end: str | StringValue) -> ir.BooleanValue`

Determine if `self` ends with `end`.

Parameters
----------
end
    Suffix to check for

Examples
--------
>>> import ibis
>>> text = ibis.literal('Ibis project')
>>> text.endswith('project')
EndsWith('Ibis project', end='project')

Returns
-------
BooleanValue
    Boolean indicating whether `self` ends with `end`

#### `find`

`find(substr: str | StringValue, start: int | ir.IntegerValue | None = None, end: int | ir.IntegerValue | None = None) -> ir.IntegerValue`

Return the position of the first occurence of substring.

Parameters
----------
substr
    Substring to search for
start
    Zero based index of where to start the search
end
    Zero based index of where to stop the search. Currently not
    implemented.

Returns
-------
IntegerValue
    Position of `substr` in `arg` starting from `start`

#### `find_in_set`

`find_in_set(str_list: Sequence[str]) -> ir.IntegerValue`

Find the first occurence of `str_list` within a list of strings.

No string in `str_list` can have a comma.

Parameters
----------
str_list
    Sequence of strings

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(strings='string'))
>>> result = table.strings.find_in_set(['a', 'b'])
>>> result
r0 := UnboundTable: unbound_table_0
  strings string
FindInSet(needle=r0.strings, values=[ValueList(values=['a', 'b'])])

Returns
-------
IntegerValue
    Position of `str_list` in `self`. Returns -1 if `self` isn't found
    or if `self` contains `','`.

#### `hashbytes`

`hashbytes(how: Literal['md5', 'sha1', 'sha256', 'sha512'] = 'sha256') -> ir.BinaryValue`

Compute the binary hash value of the input.

Parameters
----------
how
    Hash algorithm to use

Returns
-------
BinaryValue
    Binary expression

#### `ilike`

`ilike(patterns: str | StringValue | Iterable[str | StringValue]) -> ir.BooleanValue`

Match `patterns` against `self`, case-insensitive.

This function is modeled after SQL's `ILIKE` directive. Use `%` as a
multiple-character wildcard or `_` as a single-character wildcard.

Use `re_search` or `rlike` for regular expression-based matching.

Parameters
----------
patterns
    If `pattern` is a list, then if any pattern matches the input then
    the corresponding row in the output is `True`.

Returns
-------
BooleanValue
    Column indicating matches

#### `join`

`join(strings: Sequence[str | StringValue]) -> StringValue`

Join a list of strings using `self` as the separator.

Parameters
----------
strings
    Strings to join with `arg`

Examples
--------
>>> import ibis
>>> sep = ibis.literal(',')
>>> result = sep.join(['a', 'b', 'c'])
>>> result
StringJoin(sep=',', [ValueList(values=['a', 'b', 'c'])])

Returns
-------
StringValue
    Joined string

#### `left`

`left(nchars: int | ir.IntegerValue) -> StringValue`

Return the `nchars` left-most characters.

Parameters
----------
nchars
    Maximum number of characters to return

Returns
-------
StringValue
    Characters from the start

#### `length`

`length() -> ir.IntegerValue`

Compute the length of a string.

Returns
-------
IntegerValue
    The length of the input

#### `like`

`like(patterns: str | StringValue | Iterable[str | StringValue]) -> ir.BooleanValue`

Match `patterns` against `self`, case-sensitive.

This function is modeled after the SQL `LIKE` directive. Use `%` as a
multiple-character wildcard or `_` as a single-character wildcard.

Use `re_search` or `rlike` for regular expression-based matching.

Parameters
----------
patterns
    If `pattern` is a list, then if any pattern matches the input then
    the corresponding row in the output is `True`.

Returns
-------
BooleanValue
    Column indicating matches

#### `lower`

`lower() -> StringValue`

Convert string to all lowercase.

Returns
-------
StringValue
    Lowercase string

#### `lpad`

`lpad(length: int | ir.IntegerValue, pad: str | StringValue = ' ') -> StringValue`

Pad `arg` by truncating on the right or padding on the left.

Parameters
----------
length
    Length of output string
pad
    Pad character

Returns
-------
StringValue
    Padded string

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(strings='string'))
>>> expr = table.strings.lpad(5, '-')
>>> expr
r0 := UnboundTable: unbound_table_1
  strings string
LPad(r0.strings, length=5, pad='-')
>>> expr = ibis.literal('a').lpad(5, '-')  # 'a' becomes '----a'
>>> expr
LPad('a', length=5, pad='-')
>>> expr = ibis.literal('abcdefg').lpad(5, '-')  # 'abcdefg' becomes 'abcde'
>>> expr
LPad('abcdefg', length=5, pad='-')

#### `lstrip`

`lstrip() -> StringValue`

Remove whitespace from the left side of string.

Returns
-------
StringValue
    Left-stripped string

#### `parse_url`

`parse_url(extract: Literal['PROTOCOL', 'HOST', 'PATH', 'REF', 'AUTHORITY', 'FILE', 'USERINFO', 'QUERY'], key: str | None = None) -> StringValue`

Parse a URL and extract its components.

`key` can be used to extract query values when `extract == 'QUERY'`

Parameters
----------
extract
    Component of URL to extract
key
    Query component to extract

Examples
--------
>>> url = "https://www.youtube.com/watch?v=kEuEcWfewf8&t=10"
>>> parse_url(url, 'QUERY', 'v')  # doctest: +SKIP
'kEuEcWfewf8'

Returns
-------
StringValue
    Extracted string value

#### `re_extract`

`re_extract(pattern: str | StringValue, index: int | ir.IntegerValue) -> StringValue`

Return the specified match at `index` from a regex `pattern`.

Parameters
----------
pattern
    Reguar expression string
index
    Zero-based index of match to return

Returns
-------
StringValue
    Extracted match

#### `re_replace`

`re_replace(pattern: str | StringValue, replacement: str | StringValue) -> StringValue`

Replace match found by regex `pattern` with `replacement`.

Parameters
----------
pattern
    Regular expression string
replacement
    Replacement string or regular expression

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(strings='string'))
>>> result = table.strings.replace('(b+)', r'<>')  # 'aaabbbaa' becomes 'aaa<bbb>aaa'
>>> result
r0 := UnboundTable: unbound_table_1
  strings string
StringReplace(r0.strings, pattern='(b+)', replacement='<\1>')

Returns
-------
StringValue
    Modified string

#### `re_search`

`re_search(pattern: str | StringValue) -> ir.BooleanValue`

Return whether the values match `pattern`.

Returns `True` if the regex matches a string and `False` otherwise.

Parameters
----------
pattern
    Regular expression use for searching

Returns
-------
BooleanValue
    Indicator of matches

#### `repeat`

`repeat(n: int | ir.IntegerValue) -> StringValue`

Repeat a string `n` times.

Parameters
----------
n
    Number of repetitions

Returns
-------
StringValue
    Repeated string

#### `replace`

`replace(pattern: StringValue, replacement: StringValue) -> StringValue`

Replace each exact match of `pattern` with `replacement`.

Parameters
----------
pattern
    String pattern
replacement
    String replacement

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(strings='string'))
>>> result = table.strings.replace('aaa', 'foo')  # 'aaabbbaaa' becomes 'foobbbfoo'
>>> result
r0 := UnboundTable: unbound_table_1
  strings string
StringReplace(r0.strings, pattern='aaa', replacement='foo')

Returns
-------
StringVulae
    Replaced string

#### `reverse`

`reverse() -> StringValue`

Reverse the characters of a string.

Returns
-------
StringValue
    Reversed string

#### `right`

`right(nchars: int | ir.IntegerValue) -> StringValue`

Return up to `nchars` from the end of each string.

Parameters
----------
nchars
    Maximum number of characters to return

Returns
-------
StringValue
    Characters from the end

#### `rpad`

`rpad(length: int | ir.IntegerValue, pad: str | StringValue = ' ') -> StringValue`

Pad `self` by truncating or padding on the right.

Parameters
----------
self
    String to pad
length
    Length of output string
pad
    Pad character

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(string_col='string'))
>>> expr = table.string_col.rpad(5, '-')
>>> expr
r0 := UnboundTable: unbound_table_2
  string_col string
RPad(r0.string_col, length=5, pad='-')
>>> expr = ibis.literal('a').rpad(5, '-')  # 'a' becomes 'a----'
>>> expr
RPad('a', length=5, pad='-')
>>> expr = ibis.literal('abcdefg').rpad(5, '-')  # 'abcdefg' becomes 'abcde'
>>> expr
RPad('abcdefg', length=5, pad='-')

Returns
-------
StringValue
    Padded string

#### `rstrip`

`rstrip() -> StringValue`

Remove whitespace from the right side of string.

Returns
-------
StringValue
    Right-stripped string

#### `split`

`split(delimiter: str | StringValue) -> ir.ArrayValue`

Split as string on `delimiter`.

Parameters
----------
delimiter
    Value to split by

Returns
-------
ArrayValue
    The string split by `delimiter`

#### `startswith`

`startswith(start: str | StringValue) -> ir.BooleanValue`

Determine whether `self` starts with `end`.

Parameters
----------
start
    prefix to check for

Examples
--------
>>> import ibis
>>> text = ibis.literal('Ibis project')
>>> text.startswith('Ibis')
StartsWith('Ibis project', start='Ibis')

Returns
-------
BooleanValue
    Boolean indicating whether `self` starts with `start`

#### `strip`

`strip() -> StringValue`

Remove whitespace from left and right sides of a string.

Returns
-------
StringValue
    Stripped string

#### `substr`

`substr(start: int | ir.IntegerValue, length: int | ir.IntegerValue | None = None) -> StringValue`

Extract a substring.

Parameters
----------
start
    First character to start splitting, indices start at 0
length
    Maximum length of each substring. If not supplied, searches the
    entire string

Returns
-------
StringValue
    Found substring

#### `to_timestamp`

`to_timestamp(format_str: str, timezone: str | None = None) -> ir.TimestampValue`

Parse a string and return a timestamp.

Parameters
----------
format_str
    Format string in `strptime` format
timezone
    A string indicating the timezone. For example `'America/New_York'`

Examples
--------
>>> import ibis
>>> date_as_str = ibis.literal('20170206')
>>> result = date_as_str.to_timestamp('%Y%m%d')
>>> result
StringToTimestamp('20170206', format_str='%Y%m%d')

Returns
-------
TimestampValue
    Parsed timestamp value

#### `translate`

`translate(from_str: StringValue, to_str: StringValue) -> StringValue`

Replace `from_str` characters in `self` characters in `to_str`.

To avoid unexpected behavior, `from_str` should be shorter than
`to_str`.

Parameters
----------
from_str
    Characters in `arg` to replace
to_str
    Characters to use for replacement

Returns
-------
StringValue
    Translated string

Examples
--------
>>> import ibis
>>> table = ibis.table(dict(string_col='string'))
>>> expr = table.string_col.translate('a', 'b')
>>> expr
r0 := UnboundTable: unbound_table_0
  string_col string
Translate(r0.string_col, from_str='a', to_str='b')
>>> expr = table.string_col.translate('a', 'bc')
>>> expr
r0 := UnboundTable: unbound_table_0
  string_col string
Translate(r0.string_col, from_str='a', to_str='bc')

#### `upper`

`upper() -> StringValue`

Convert string to all uppercase.

Returns
-------
StringValue
    Uppercase string

---



# Table Expressions

Table expressions form the basis for most Ibis expressions.

## `Table`

### Methods

#### `aggregate`

`aggregate(metrics: Sequence[ir.Scalar] | None = None, by: Sequence[ir.Value] | None = None, having: Sequence[ir.BooleanValue] | None = None, **kwargs: ir.Value) -> Table`

Aggregate a table with a given set of reductions grouping by `by`.

Parameters
----------
metrics
    Aggregate expressions
by
    Grouping expressions
having
    Post-aggregation filters
kwargs
    Named aggregate expressions

Returns
-------
Table
    An aggregate table expression

#### `alias`

`alias(alias: str) -> ir.Table`

Create a table expression with a specific name `alias`.

This method is useful for exposing an ibis expression to the underlying
backend for use in the
[`Table.sql`][ibis.expr.types.relations.Table.sql] method.

!!! note "`.alias` will create a temporary view"

    `.alias` creates a temporary view in the database.

    This side effect will be removed in a future version of ibis and
    **is not part of the public API**.

Parameters
----------
alias
    Name of the child expression

Returns
-------
Table
    An table expression

Examples
--------
>>> con = ibis.duckdb.connect("ci/ibis-testing-data/ibis_testing.ddb")
>>> t = con.table("functional_alltypes")
>>> expr = t.alias("my_t").sql("SELECT sum(double_col) FROM my_t")
>>> expr
r0 := AlchemyTable: functional_alltypes
  index           int64
    ⋮
  month           int32
r1 := View[r0]: my_t
  schema:
    index           int64
      ⋮
    month           int32
SQLStringView[r1]: _ibis_view_0
  query: 'SELECT sum(double_col) FROM my_t'
  schema:
    sum(double_col) float64

#### `asof_join`

`asof_join(left: Table, right: Table, predicates: str | ir.BooleanColumn | Sequence[str | ir.BooleanColumn] = (), by: str | ir.Column | Sequence[str | ir.Column] = (), tolerance: str | ir.IntervalScalar | None = None, *, suffixes: tuple[str, str] = ('_x', '_y')) -> Table`

Perform an "as-of" join between `left` and `right`.

Similar to a left join except that the match is done on nearest key
rather than equal keys.

Optionally, match keys with `by` before joining with `predicates`.

Parameters
----------
left
    Table expression
right
    Table expression
predicates
    Join expressions
by
    column to group by before joining
tolerance
    Amount of time to look behind when joining
suffixes
    Left and right suffixes that will be used to rename overlapping
    columns.

Returns
-------
Table
    Table expression

#### `count`

`count() -> ir.IntegerScalar`

Compute the number of rows in the table.

Returns
-------
IntegerScalar
    Number of rows in the table

#### `cross_join`

`cross_join(left: Table, right: Table, *rest: Table, suffixes: tuple[str, str] = ('_x', '_y')) -> Table`

Compute the cross join of a sequence of tables.

Parameters
----------
left
    Left table
right
    Right table
rest
    Additional tables to cross join
suffixes
    Left and right suffixes that will be used to rename overlapping
    columns.

Returns
-------
Table
    Cross join of `left`, `right` and `rest`

Examples
--------
>>> import ibis
>>> schemas = [(name, 'int64') for name in 'abcde']
>>> a, b, c, d, e = [
...     ibis.table([(name, type)], name=name) for name, type in schemas
... ]
>>> joined1 = ibis.cross_join(a, b, c, d, e)
>>> joined1
r0 := UnboundTable[e]
  e int64
r1 := UnboundTable[d]
  d int64
r2 := UnboundTable[c]
  c int64
r3 := UnboundTable[b]
  b int64
r4 := UnboundTable[a]
  a int64
r5 := CrossJoin[r3, r2]
r6 := CrossJoin[r5, r1]
r7 := CrossJoin[r6, r0]
CrossJoin[r4, r7]

#### `difference`

`difference(*tables: Table, distinct: bool = True, **kwargs) -> Table`

Compute the set difference of multiple table expressions.

The input tables must have identical schemas.

Parameters
----------
*tables
    One or more table expressions
distinct
    Only diff distinct rows not occurring in the calling table

Returns
-------
Table
    The rows present in `self` that are not present in `tables`.

#### `distinct`

`distinct() -> Table`

Compute the set of unique rows in the table.

#### `drop`

`drop(fields: str | Sequence[str]) -> Table`

Remove fields from a table.

Parameters
----------
fields
    Fields to drop

Returns
-------
Table
    Expression without `fields`

#### `dropna`

`dropna(subset: Sequence[str] | None = None, how: Literal['any', 'all'] = 'any') -> Table`

Remove rows with null values from the table.

Parameters
----------
subset
    Columns names to consider when dropping nulls. By default all columns
    are considered.
how
    Determine whether a row is removed if there is at least one null
    value in the row ('any'), or if all row values are null ('all').
    Options are 'any' or 'all'. Default is 'any'.

Examples
--------
>>> import ibis
>>> t = ibis.table(dict(a='int64', b='string'), name='t')
>>> t = t.dropna()  # Drop all rows where any values are null
>>> t
r0 := UnboundTable: t
  a int64
  b string
DropNa[r0]
  how: 'any'
>>> t.dropna(how='all')  # Only drop rows where all values are null
r0 := UnboundTable: t
  a int64
  b string
r1 := DropNa[r0]
  how: 'all'
>>> t.dropna(subset=['a'], how='all')  # Only drop rows where all values in column 'a' are null  # noqa: E501
r0 := UnboundTable: t
  a int64
  b string
DropNa[r0]
  how: 'all'
  subset:
    r0.a

Returns
-------
Table
    Table expression

#### `fillna`

`fillna(replacements: ir.Scalar | Mapping[str, ir.Scalar]) -> Table`

Fill null values in a table expression.

Parameters
----------
replacements
    Value with which to fill the nulls. If passed as a mapping, the keys
    are column names that map to their replacement value. If passed
    as a scalar, all columns are filled with that value.

Notes
-----
There is potential lack of type stability with the `fillna` API. For
example, different library versions may impact whether or not a given
backend promotes integer replacement values to floats.

Examples
--------
>>> import ibis
>>> import ibis.expr.datatypes as dt
>>> t = ibis.table([('a', 'int64'), ('b', 'string')])
>>> t = t.fillna(0.0)  # Replace nulls in all columns with 0.0
>>> t.fillna({c: 0.0 for c, t in t.schema().items() if t == dt.float64})
r0 := UnboundTable[unbound_table_...]
  a int64
  b string
r1 := FillNa[r0]
  replacements:
    0.0
FillNa[r1]
  replacements:
    frozendict({})

Returns
-------
Table
    Table expression

#### `filter`

`filter(predicates: ir.BooleanValue | Sequence[ir.BooleanValue]) -> Table`

Select rows from `table` based on `predicates`.

Parameters
----------
predicates
    Boolean value expressions used to select rows in `table`.

Returns
-------
Table
    Filtered table expression

#### `get_column`

`get_column(name: str) -> Column`

Get a reference to a single column from the table

Returns
-------
Column
    A column named `name`.

#### `get_columns`

`get_columns(iterable: Iterable[str]) -> list[Column]`

Get multiple columns from the table

Examples
--------
>>> import ibis
>>> table = ibis.table(
...    [
...        ('a', 'int64'),
...        ('b', 'string'),
...        ('c', 'timestamp'),
...        ('d', 'float'),
...    ],
...    name='t'
... )
>>> a, b, c = table.get_columns(['a', 'b', 'c'])

Returns
-------
list[ir.Column]
    List of column expressions

#### `group_by`

`group_by(by=None, **additional_grouping_expressions: Any) -> GroupedTable`

Create a grouped table expression.

Parameters
----------
by
    Grouping expressions
additional_grouping_expressions
    Named grouping expressions

Examples
--------
>>> import ibis
>>> from ibis import _
>>> t = ibis.table(dict(a='int32', b='timestamp', c='double'), name='t')
>>> t.group_by([_.a, _.b]).aggregate(sum_of_c=_.c.sum())
r0 := UnboundTable: t
  a int32
  b timestamp
  c float64
Aggregation[r0]
  metrics:
    sum_of_c: Sum(r0.c)
  by:
    a: r0.a
    b: r0.b

Returns
-------
GroupedTable
    A grouped table expression

#### `head`

`head(n: int = 5) -> Table`

Select the first `n` rows of a table.

The result set is not deterministic without a sort.

Parameters
----------
n
    Number of rows to include, defaults to 5

Returns
-------
Table
    `table` limited to `n` rows

#### `info`

`info(buf: IO[str] | None = None) -> None`

Show column names, types and null counts.

Parameters
----------
buf
    A writable buffer, defaults to stdout

#### `intersect`

`intersect(*tables: Table, distinct: bool = True, **kwargs) -> Table`

Compute the set intersection of multiple table expressions.

The input tables must have identical schemas.

Parameters
----------
*tables
    One or more table expressions
distinct
    Only return distinct rows

Returns
-------
Table
    A new table containing the intersection of all input tables.

#### `join`

`join(left: Table, right: Table, predicates: str | Sequence[str | tuple[str | ir.Column, str | ir.Column] | ir.BooleanColumn] = (), how: Literal['inner', 'left', 'outer', 'right', 'semi', 'anti', 'any_inner', 'any_left', 'left_semi'] = 'inner', *, suffixes: tuple[str, str] = ('_x', '_y')) -> Table`

Perform a join between two tables.

Parameters
----------
left
    Left table to join
right
    Right table to join
predicates
    Boolean or column names to join on
how
    Join method
suffixes
    Left and right suffixes that will be used to rename overlapping
    columns.

#### `limit`

`limit(n: int, offset: int = 0) -> Table`

Select the first `n` rows starting at `offset`.

Parameters
----------
n
    Number of rows to include
offset
    Number of rows to skip first

Returns
-------
Table
    The first `n` rows of `table` starting at `offset`

#### `materialize`

`materialize() -> Table`

#### `mutate`

`mutate(exprs: Sequence[ir.Expr] | None = None, **mutations: ir.Value) -> Table`

Add columns to a table expression.

Parameters
----------
exprs
    List of named expressions to add as columns
mutations
    Named expressions using keyword arguments

Returns
-------
Table
    Table expression with additional columns

Examples
--------
Using keywords arguments to name the new columns

>>> import ibis
>>> table = ibis.table(
...     [('foo', 'double'), ('bar', 'double')],
...     name='t'
... )
>>> expr = table.mutate(qux=table.foo + table.bar, baz=5)
>>> expr
r0 := UnboundTable[t]
  foo float64
  bar float64
Selection[r0]
  selections:
    r0
    baz: 5
    qux: r0.foo + r0.bar

Use the [`name`][ibis.expr.types.generic.Value.name] method to name
the new columns.

>>> new_columns = [ibis.literal(5).name('baz',),
...                (table.foo + table.bar).name('qux')]
>>> expr2 = table.mutate(new_columns)
>>> expr.equals(expr2)
True

#### `prevent_rewrite`

`prevent_rewrite(client=None) -> Table`

Prevent optimization from happening below this expression.

Only valid on SQL-string generating backends.

Parameters
----------
client
    A client to use to create the SQLQueryResult operation. This can be
    useful if you're compiling an expression that derives from an
    `UnboundTable` operation.

Returns
-------
Table
    An opaque SQL query

#### `relabel`

`relabel(substitutions: Mapping[str, str]) -> Table`

Change table column names, otherwise leaving table unaltered.

Parameters
----------
substitutions
    Name mapping

Returns
-------
Table
    A relabeled table expression

#### `rowid`

`rowid() -> ir.IntegerValue`

A numbering expression representing the row number of the results.

It can be 0 or 1 indexed depending on the backend. Check the backend
documentation for specifics.

Notes
-----
This function is different from the window function `row_number`
(even if they are conceptually the same), and different from `rowid` in
backends where it represents the physical location
(e.g. Oracle or PostgreSQL's ctid).

Returns
-------
IntegerColumn
    An integer column

Examples
--------
>>> my_table[my_table.rowid(), my_table.name].execute()  # doctest: +SKIP
1|Ibis
2|pandas
3|Dask

#### `schema`

`schema() -> sch.Schema`

Get the schema for this table (if one is known)

Returns
-------
Schema
    The table's schema.

#### `select`

`select(*exprs: ir.Value | str | Iterable[ir.Value | str], **named_exprs: ir.Value | str) -> Table`

Compute a new table expression using `exprs`.

Passing an aggregate function to this method will broadcast the
aggregate's value over the number of rows in the table and
automatically constructs a window function expression. See the examples
section for more details.

For backwards compatibility the keyword argument `exprs` is reserved
and cannot be used to name an expression. This behavior will be removed
in v4.

Parameters
----------
exprs
    Column expression, string, or list of column expressions and
    strings.

Returns
-------
Table
    Table expression

Examples
--------
Simple projection

>>> import ibis
>>> t = ibis.table(dict(a="int64", b="double"), name='t')
>>> proj = t.select(t.a, b_plus_1=t.b + 1)
>>> proj
r0 := UnboundTable[t]
  a int64
  b float64
Selection[r0]
  selections:
    a:        r0.a
    b_plus_1: r0.b + 1
>>> proj2 = t.select("a", b_plus_1=t.b + 1)
>>> proj.equals(proj2)
True

Aggregate projection

>>> agg_proj = t.select(sum_a=t.a.sum(), mean_b=t.b.mean())
>>> agg_proj
r0 := UnboundTable[t]
  a int64
  b float64
Selection[r0]
  selections:
    sum_a:  Window(Sum(r0.a), window=Window(how='rows'))
    mean_b: Window(Mean(r0.b), window=Window(how='rows'))

Note the `Window` objects here.

Their existence means that the result of the aggregation will be
broadcast across the number of rows in the input column.
The purpose of this expression rewrite is to make it easy to write
column/scalar-aggregate operations like

>>> t.select(demeaned_a=t.a - t.a.mean())
r0 := UnboundTable[t]
  a int64
  b float64
Selection[r0]
  selections:
    demeaned_a: r0.a - Window(Mean(r0.a), window=Window(how='rows'))

#### `set_column`

`set_column(name: str, expr: ir.Value) -> Table`

Replace an existing column with a new expression.

Parameters
----------
name
    Column name to replace
expr
    New data for column

Returns
-------
Table
    Table expression with new columns

#### `sort_by`

`sort_by(sort_exprs: str | ir.Column | ir.SortKey | tuple[str | ir.Column, bool] | Sequence[tuple[str | ir.Column, bool]]) -> Table`

Sort table by `sort_exprs`

Parameters
----------
sort_exprs
    Sort specifications

Examples
--------
>>> import ibis
>>> t = ibis.table(dict(a='int64', b='string'))
>>> t.sort_by(['a', ibis.desc('b')])
r0 := UnboundTable: unbound_table_0
  a int64
  b string
Selection[r0]
  sort_keys:
     asc|r0.a
    desc|r0.b

Returns
-------
Table
    Sorted table

#### `sql`

`sql(query: str) -> ir.Table`

Run a SQL query against a table expression.

!!! note "The SQL string is backend specific"

    `query` must be valid SQL for the execution backend the expression
    will run against

See [`Table.alias`][ibis.expr.types.relations.Table.alias] for
details on using named table expressions in a SQL string.

Parameters
----------
query
    Query string

Returns
-------
Table
    An opaque table expression

Examples
--------
>>> con = ibis.duckdb.connect("ci/ibis-testing-data/ibis_testing.ddb")
>>> t = con.table("functional_alltypes")
>>> expr = t.sql("SELECT sum(double_col) FROM functional_alltypes")
>>> expr
r0 := AlchemyTable: functional_alltypes
  index           int64
    ⋮
  month           int32
SQLStringView[r0]: _ibis_view_1
  query: 'SELECT sum(double_col) FROM functional_alltypes'
  schema:
    sum(double_col) float64

#### `to_array`

`to_array() -> ir.Column`

View a single column table as an array.

Returns
-------
Value
    A single column view of a table

#### `union`

`union(*tables: Table, distinct: bool = False, **kwargs) -> Table`

Compute the set union of multiple table expressions.

The input tables must have identical schemas.

Parameters
----------
*tables
    One or more table expressions
distinct
    Only return distinct rows

Returns
-------
Table
    A new table containing the union of all input tables.

#### `unpack`

`unpack(*columns: str) -> Table`

Project the struct fields of each of `columns` into `self`.

Existing fields are retained in the projection.

Parameters
----------
columns
    String column names to project into `self`.

Returns
-------
Table
    The child table with struct fields of each of `columns` projected.

Examples
--------
>>> schema = dict(a="struct<b: float, c: string>", d="string")
>>> t = ibis.table(schema, name="t")
>>> t
UnboundTable: t
  a struct<b: float64, c: string>
  d string
>>> t.unpack("a")
r0 := UnboundTable: t
  a struct<b: float64, c: string>
  d string

Selection[r0]
  selections:
    b: StructField(r0.a, field='b')
    c: StructField(r0.a, field='c')
    d: r0.d

See Also
--------
ibis.expr.types.structs.StructValue.lift

#### `view`

`view() -> Table`

Create a new table expression distinct from the current one.

Use this API for any self-referencing operations like a self-join.

Returns
-------
Table
    Table expression

---

## `GroupedTable`

### Methods

#### `aggregate`

`aggregate(metrics=None, **kwds)`

#### `count`

`count(metric_name: str = 'count') -> ir.Table`

Computing the number of rows per group.

Parameters
----------
metric_name
    Name to use for the row count metric

Returns
-------
Table
    The aggregated table

#### `having`

`having(expr: ir.BooleanScalar) -> GroupedTable`

Add a post-aggregation result filter `expr`.

Parameters
----------
expr
    An expression that filters based on an aggregate value.

Returns
-------
GroupedTable
    A grouped table expression

#### `mutate`

`mutate(exprs: ir.Value | Sequence[ir.Value] | None = None, **kwds: ir.Value)`

Return a table projection with window functions applied.

Any arguments can be functions.

Parameters
----------
exprs
    List of expressions
kwds
    Expressions

Examples
--------
>>> import ibis
>>> t = ibis.table([
...     ('foo', 'string'),
...     ('bar', 'string'),
...     ('baz', 'double'),
... ], name='t')
>>> t
UnboundTable[t]
  foo string
  bar string
  baz float64
>>> expr = (t.group_by('foo')
...          .order_by(ibis.desc('bar'))
...          .mutate(qux=lambda x: x.baz.lag(),
...                  qux2=t.baz.lead()))
>>> print(expr)
r0 := UnboundTable[t]
  foo string
  bar string
  baz float64
Selection[r0]
  selections:
    r0
    qux:  Window(Lag(r0.baz), window=Window(group_by=[r0.foo], order_by=[desc|r0.bar], how='rows'))
    qux2: Window(Lead(r0.baz), window=Window(group_by=[r0.foo], order_by=[desc|r0.bar], how='rows'))

Returns
-------
Table
    A table expression with window functions applied

#### `order_by`

`order_by(expr: ir.Value | Iterable[ir.Value]) -> GroupedTable`

Sort a grouped table expression by `expr`.

Notes
-----
This API call is ignored in aggregations.

Parameters
----------
expr
    Expressions to order the results by

Returns
-------
GroupedTable
    A sorted grouped GroupedTable

#### `over`

`over(window: _window.Window) -> GroupedTable`

Add a window frame clause to be applied to child analytic
expressions.

Parameters
----------
window
    Window to add to child analytic expressions

Returns
-------
GroupedTable
    A new grouped table expression

#### `projection`

`projection(exprs)`

Project new columns out of the grouped table.

See Also
--------
ibis.expr.groupby.GroupedTable.mutate

---



# Temporal Expression APIs

All temporal operations are valid for both scalars and columns.

## `TemporalValue`

### Methods

#### `strftime`

`strftime(format_str: str) -> ir.StringValue`

Format timestamp according to `format_str`.

Format string may depend on the backend, but we try to conform to ANSI
`strftime`.

Parameters
----------
format_str
    `strftime` format string

Returns
-------
StringValue
    Formatted version of `arg`

---

## `TimestampValue`

### Methods

#### `date`

`date() -> DateValue`

Return the date component of the expression.

Returns
-------
DateValue
    The date component of `self`

#### `truncate`

`truncate(unit: Literal['Y', 'Q', 'M', 'W', 'D', 'h', 'm', 's', 'ms', 'us', 'ns']) -> TimestampValue`

Truncate timestamp expression to units of `unit`.

Parameters
----------
unit
    Unit to truncate to

Returns
-------
TimestampValue
    Truncated timestamp expression

---

## `DateValue`

### Methods

#### `truncate`

`truncate(unit: Literal['Y', 'Q', 'M', 'W', 'D']) -> DateValue`

Truncate date expression to units of `unit`.

Parameters
----------
unit
    Unit to truncate `arg` to

Returns
-------
DateValue
    Truncated date value expression

---

## `TimeValue`

### Methods

#### `truncate`

`truncate(unit: Literal['h', 'm', 's', 'ms', 'us', 'ns']) -> TimeValue`

Truncate the expression to a time expression in units of `unit`.

Commonly used for time series resampling.

Parameters
----------
unit
    The unit to truncate to

Returns
-------
TimeValue
    `self` truncated to `unit`

---

## `IntervalValue`

### Methods

#### `negate`

`negate() -> ir.IntervalValue`

Negate an interval expression.

Returns
-------
IntervalValue
    A negated interval value expression

#### `to_unit`

`to_unit(target_unit: str) -> IntervalValue`

Convert this interval to units of `target_unit`.

---



# Top-level APIs

These methods and objects are available directly in the `ibis` module.

## `NA`

`NA` is the null scalar.

## `and_`

#### `and_`

`and_(*predicates: ir.BooleanValue) -> ir.BooleanValue`

Combine multiple predicates using `&`.

Parameters
----------
predicates
    Boolean value expressions

Returns
-------
BooleanValue
    A new predicate that evaluates to True if all composing predicates are
    True. If no predicates were provided, returns True.

## `array`

#### `array`

`array(values: Iterable[V], type: str | dt.DataType | None = None) -> ArrayValue`

Create an array expression.

If the input expressions are all column expressions, then the output will
be an `ArrayColumn`. The input columns will be concatenated row-wise to
produce each array in the output array column. Each array will have length
_n_, where _n_ is the number of input columns. All input columns should be
of the same datatype.

If the input expressions are Python literals, then the output will be a
single `ArrayScalar` of length _n_, where _n_ is the number of input
values. This is equivalent to

```python
values = [1, 2, 3]
ibis.literal(values)
```

Parameters
----------
values
    An iterable of Ibis expressions or a list of Python literals
type
    An instance of `ibis.expr.datatypes.DataType` or a string indicating
    the ibis type of `value`.

Returns
-------
ArrayValue
    An array column (if the inputs are column expressions), or an array
    scalar (if the inputs are Python literals)

Examples
--------
Create an array column from column expressions
>>> import ibis
>>> t = ibis.table([('a', 'int64'), ('b', 'int64')], name='t')
>>> result = ibis.array([t.a, t.b])

Create an array scalar from Python literals
>>> import ibis
>>> result = ibis.array([1.0, 2.0, 3.0])

## `asc`

#### `asc`

`asc(expr: ir.Column | str) -> ir.SortExpr | ops.DeferredSortKey`

Create a ascending sort key from `asc` or column name.

Parameters
----------
expr
    The expression or column name to use for sorting

Examples
--------
>>> import ibis
>>> t = ibis.table(dict(g='string'), name='t')
>>> t.group_by('g').size('count').sort_by(ibis.asc('count'))
r0 := UnboundTable: t
  g string
r1 := Aggregation[r0]
  metrics:
    count: Count(t)
  by:
    g: r0.g
Selection[r1]
  sort_keys:
    asc|r1.count

Returns
-------
ir.SortExpr | ops.DeferredSortKey
    A sort expression or deferred sort key

## `case`

#### `case`

`case() -> bl.SearchedCaseBuilder`

Begin constructing a case expression.

Notes
-----
Use the `.when` method on the resulting object followed by .end to create a
complete case.

Examples
--------
>>> import ibis
>>> cond1 = ibis.literal(1) == 1
>>> cond2 = ibis.literal(2) == 1
>>> (ibis.case()
...  .when(cond1, 3)
...  .when(cond2, 4).end())
>>> SearchedCase(cases=[ValueList(values=[1 == 1, 2 == 1])], results=[ValueList(values=[3, 4])], default=Cast(None, to=int8))

Returns
-------
SearchedCaseBuilder
    A builder object to use for constructing a case expression.

## `coalesce`

### Methods

---

## `cumulative_window`

#### `cumulative_window`

`cumulative_window(group_by=None, order_by=None) -> Window`

Create a cumulative window for use with window functions.

All window frames / ranges are inclusive.

Parameters
----------
group_by
    Grouping key
order_by
    Ordering key

Returns
-------
Window
    A window frame

## `date`

#### `date`

`date(value) -> DateValue`

Return a date literal if `value` is coercible to a date.

Parameters
----------
value
    Date string

Returns
-------
DateScalar
    A date expression

## `desc`

#### `desc`

`desc(expr: ir.Column | str) -> ir.SortExpr | ops.DeferredSortKey`

Create a descending sort key from `expr` or column name.

Parameters
----------
expr
    The expression or column name to use for sorting

Examples
--------
>>> import ibis
>>> t = ibis.table(dict(g='string'), name='t')
>>> t.group_by('g').size('count').sort_by(ibis.desc('count'))
r0 := UnboundTable: t
  g string
r1 := Aggregation[r0]
  metrics:
    count: Count(t)
  by:
    g: r0.g
Selection[r1]
  sort_keys:
    desc|r1.count

Returns
-------
ir.SortExpr | ops.DeferredSortKey
    A sort expression or deferred sort key

## `difference`

### Methods

---

## `greatest`

### Methods

---

## `ifelse`

### Methods

---

## `intersect`

### Methods

---

## `interval`

#### `interval`

`interval(value: int | datetime.timedelta | None = None, unit: str = 's', years: int | None = None, quarters: int | None = None, months: int | None = None, weeks: int | None = None, days: int | None = None, hours: int | None = None, minutes: int | None = None, seconds: int | None = None, milliseconds: int | None = None, microseconds: int | None = None, nanoseconds: int | None = None) -> ir.IntervalScalar`

Return an interval literal expression.

Parameters
----------
value
    Interval value. If passed, must be combined with `unit`.
unit
    Unit of `value`
years
    Number of years
quarters
    Number of quarters
months
    Number of months
weeks
    Number of weeks
days
    Number of days
hours
    Number of hours
minutes
    Number of minutes
seconds
    Number of seconds
milliseconds
    Number of milliseconds
microseconds
    Number of microseconds
nanoseconds
    Number of nanoseconds

Returns
-------
IntervalScalar
    An interval expression

## `least`

### Methods

---

## `literal`

#### `literal`

`literal(value: Any, type: dt.DataType | str | None = None) -> Scalar`

Create a scalar expression from a Python value.

!!! tip "Use specific functions for arrays, structs and maps"

    Ibis supports literal construction of arrays using the following
    functions:

    1. [`ibis.array`][ibis.array]
    1. [`ibis.struct`][ibis.struct]
    1. [`ibis.map`][ibis.map]

    Constructing these types using `literal` will be deprecated in a future
    release.

Parameters
----------
value
    A Python value
type
    An instance of [`DataType`][ibis.expr.datatypes.DataType] or a string
    indicating the ibis type of `value`. This parameter can be used
    in cases where ibis's type inference isn't sufficient for discovering
    the type of `value`.

Returns
-------
Scalar
    An expression representing a literal value

Examples
--------
Construct an integer literal

>>> import ibis
>>> x = ibis.literal(42)
>>> x.type()
Int8(nullable=True)

Construct a `float64` literal from an `int`

>>> y = ibis.literal(42, type='double')
>>> y.type()
Float64(nullable=True)

Ibis checks for invalid types

>>> ibis.literal('foobar', type='int64')  # doctest: +ELLIPSIS
Traceback (most recent call last):
  ...
TypeError: Value 'foobar' cannot be safely coerced to int64

## `map`

#### `map`

`map(value: Iterable[tuple[K, V]] | Mapping[K, V], type: str | dt.DataType | None = None) -> MapValue`

Create a map literal from a [`dict`][dict] or other mapping.

Parameters
----------
value
    the literal map value
type
    An instance of `ibis.expr.datatypes.DataType` or a string indicating
    the ibis type of `value`.

Returns
-------
MapScalar
    An expression representing a literal map (associative array with
    key/value pairs of fixed types)

Examples
--------
Create a map literal from a dict with the type inferred
>>> import ibis
>>> t = ibis.map(dict(a=1, b=2))

Create a map literal from a dict with the specified type
>>> import ibis
>>> t = ibis.map(dict(a=1, b=2), type='map<string, double>')

## `negate`

### Methods

---

## `now`

#### `now`

`now() -> ir.TimestampScalar`

Return an expression that will compute the current timestamp.

Returns
-------
TimestampScalar
    A "now" expression

## `null`

#### `null`

`null()`

Create a NULL/NA scalar

## `or_`

#### `or_`

`or_(*predicates: ir.BooleanValue) -> ir.BooleanValue`

Combine multiple predicates using `|`.

Parameters
----------
predicates
    Boolean value expressions

Returns
-------
BooleanValue
    A new predicate that evaluates to True if any composing predicates are
    True. If no predicates were provided, returns False.

## `param`

#### `param`

`param(type: dt.DataType) -> ir.Scalar`

Create a deferred parameter of a given type.

Parameters
----------
type
    The type of the unbound parameter, e.g., double, int64, date, etc.

Returns
-------
Scalar
    A scalar expression backend by a parameter

Examples
--------
>>> import ibis
>>> start = ibis.param('date')
>>> end = ibis.param('date')
>>> schema = dict(timestamp_col='timestamp', value='double')
>>> t = ibis.table(schema, name='t')
>>> predicates = [t.timestamp_col >= start, t.timestamp_col <= end]
>>> t.filter(predicates).value.sum()
r0 := UnboundTable: t
  timestamp_col timestamp
  value         float64
r1 := Selection[r0]
  predicates:
    r0.timestamp_col >= $(date)
    r0.timestamp_col <= $(date)
sum: Sum(r1.value)

## `show_sql`

#### `show_sql`

`show_sql(expr: ir.Expr, dialect: str | None = None, file: IO[str] | None = None) -> None`

Pretty-print the compiled SQL string of an expression.

If a dialect cannot be inferred and one was not passed, duckdb
will be used as the dialect

Parameters
----------
expr
    Ibis expression whose SQL will be printed
dialect
    String dialect. This is typically not required, but can be useful if
    ibis cannot infer the backend dialect.
file
    File to write output to

Examples
--------
>>> import ibis
>>> from ibis import _
>>> t = ibis.table(dict(a="int"), name="t")
>>> expr = t.select(c=_.a * 2)
>>> ibis.show_sql(expr)  # duckdb dialect by default
SELECT
  t0.a * CAST(2 AS SMALLINT) AS c
FROM t AS t0
>>> ibis.show_sql(expr, dialect="mysql")
SELECT
  t0.a * 2 AS c
FROM t AS t0

## `to_sql`

#### `to_sql`

`to_sql(expr: ir.Expr, dialect: str | None = None) -> str`

Return the formatted SQL string for an expression.

Parameters
----------
expr
    Ibis expression.
dialect
    SQL dialect to use for compilation.

Returns
-------
str
    Formatted SQL string

## `random`

#### `random`

`random() -> ir.FloatingScalar`

Return a random floating point number in the range [0.0, 1.0).

Similar to [`random.random`][random.random] in the Python standard library.

Returns
-------
FloatingScalar
    Random float value expression

## `range_window`

#### `range_window`

`range_window(preceding=None, following=None, group_by=None, order_by=None)`

Create a range-based window clause for use with window functions.

This RANGE window clause aggregates rows based upon differences in the
value of the order-by expression.

All window frames / ranges are inclusive.

Parameters
----------
preceding
    Number of preceding rows in the window
following
    Number of following rows in the window
group_by
    Grouping key
order_by
    Ordering key

Returns
-------
Window
    A window frame

## `row_number`

#### `row_number`

`row_number() -> ir.IntegerColumn`

Return an analytic function expression for the current row number.

Returns
-------
IntegerColumn
    A column expression enumerating rows

## `schema`

#### `schema`

`schema(pairs: SupportsSchema | None = None, names: Iterable[str] | None = None, types: Iterable[str | dt.DataType] | None = None) -> sch.Schema`

Validate and return a [`Schema`][ibis.expr.schema.Schema] object.

Parameters
----------
pairs
    List or dictionary of name, type pairs. Mutually exclusive with `names`
    and `types` arguments.
names
    Field names. Mutually exclusive with `pairs`.
types
    Field types. Mutually exclusive with `pairs`.

Examples
--------
>>> from ibis import schema, Schema
>>> sc = schema([('foo', 'string'),
...              ('bar', 'int64'),
...              ('baz', 'boolean')])
>>> sc = schema(names=['foo', 'bar', 'baz'],
...             types=['string', 'int64', 'boolean'])
>>> sc = schema(dict(foo="string"))
>>> sc = schema(Schema(['foo'], ['string']))  # no-op

Returns
-------
Schema
    An ibis schema

## `struct`

#### `struct`

`struct(value: Iterable[tuple[str, V]] | Mapping[str, V], type: str | dt.DataType | None = None) -> StructValue`

Create a struct literal from a [`dict`][dict] or other mapping.

Parameters
----------
value
    The underlying data for literal struct value
type
    An instance of `ibis.expr.datatypes.DataType` or a string indicating
    the ibis type of `value`.

Returns
-------
StructScalar
    An expression representing a literal struct (compound type with fields
    of fixed types)

Examples
--------
Create a struct literal from a [`dict`][dict] with the type inferred
>>> import ibis
>>> t = ibis.struct(dict(a=1, b='foo'))

Create a struct literal from a [`dict`][dict] with a specified type
>>> t = ibis.struct(dict(a=1, b='foo'), type='struct<a: float, b: string>')

## `table`

#### `table`

`table(schema: SupportsSchema | None = None, name: str | None = None) -> ir.Table`

Create a table literal or an abstract table without data.

Parameters
----------
schema
    A schema for the table
name
    Name for the table. One is generated if this value is `None`.

Returns
-------
Table
    A table expression

Examples
--------
Create a table with no data backing it

>>> t = ibis.table(schema=dict(a="int", b="string"))
>>> t
UnboundTable: unbound_table_0
  a int64
  b string

## `time`

#### `time`

`time(value) -> TimeValue`

## `timestamp`

#### `timestamp`

`timestamp(value, *args, timezone: str | None = None) -> ir.TimestampScalar`

Construct a timestamp literal if `value` is coercible to a timestamp.

Parameters
----------
value
    The value to use for constructing the timestamp
timezone
    The timezone of the timestamp

Returns
-------
TimestampScalar
    A timestamp expression

## `trailing_range_window`

#### `trailing_range_window`

`trailing_range_window(preceding, order_by, group_by=None) -> Window`

Create a trailing range window for use with window functions.

Parameters
----------
preceding
    A value expression
order_by
    Ordering key
group_by
    Grouping key

Returns
-------
Window
    A window frame

## `trailing_window`

#### `trailing_window`

`trailing_window(preceding, group_by=None, order_by=None)`

Create a trailing window for use with aggregate window functions.

Parameters
----------
preceding
    The number of preceding rows
group_by
    Grouping key
order_by
    Ordering key

Returns
-------
Window
    A window frame

## `union`

### Methods

---

## `where`

### Methods

---

## `window`

#### `window`

`window(preceding=None, following=None, group_by=None, order_by=None)`

Create a window clause for use with window functions.

The `ROWS` window clause includes peer rows based on differences in row
**number** whereas `RANGE` includes rows based on the differences in row
**value** of a single `order_by` expression.

All window frame bounds are inclusive.

Parameters
----------
preceding
    Number of preceding rows in the window
following
    Number of following rows in the window
group_by
    Grouping key
order_by
    Ordering key

Returns
-------
Window
    A window frame
