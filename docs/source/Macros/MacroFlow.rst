========
``flow``
========

.. note::

  Either ``boun`` or ``flow`` are required for a flow problem.

Flow data. Source and sink parameters are input and may be used to apply boundary conditions. Note that the alternative definitions for isothermal models apply when flow is used in conjunction with control statement **airwater **(`See Control statement airwater or air (optional) <Macro80880.html>`_). 

+-------------------------+--------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Input Variable          | Format | Default | Description                                                                                                                                                                                                                                                                                                                                                                                     |
+=========================+========+=========+=================================================================================================================================================================================================================================================================================================================================================================================================+
| Non-Isothermal model    |        |         |                                                                                                                                                                                                                                                                                                                                                                                                 |
+-------------------------+--------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SKD                     | real   | 0.      | Heat and mass source strength (kg/s), heat only (MJ/s). Negative value indicates injection into the rock mass.                                                                                                                                                                                                                                                                                  |
+-------------------------+--------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| EFLOW                   | real   | 0.      | Enthalpy of fluid injected (MJ/kg). If the fluid is flowing from the rock mass, then the in-place enthalpy is used.                                                                                                                                                                                                                                                                             |
+-------------------------+--------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                         |        |         | If EFLOW < 0, then ABS(EFLOW) is interpreted as a temperature (oC) and the enthalpy (assuming water only) calculated accordingly. In heat only problems with EFLOW < 0, the node is in contact with a large heat pipe that supplies heat to the node through an impedance AIPED so as to maintain its temperature near ABS (EFLOW). Large values (approximately 1000) of AIPED are recommended. |
+-------------------------+--------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| AIPED                   | real   | 0.      | Impedance parameter. If AIPED is nonzero, the code interprets SKD as a flowing wellbore pressure (MPa) with an impedance ABS(AIPED). If AIPED < 0, flow is only allowed out of the well. For heat only, AIPED is the thermal resistance. If AIPED = 0, SKD is flow rate. If AIPED ≠ 0 and SKD = 0 the initial value of pressure will be used for the flowing pressure.                          |
+-------------------------+--------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. note::
   If the porosity of the node is zero, then there is only a temperature solution,
   and the code forms a source proportional to the enthalpy difference.
   The source term is given by :math:`Q = AIPED \cdot (E - EFLOW)`,
   where E is the in-place enthalpy and EFLOW is a specified enthalpy.

+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+
| Isothermal model                                                                                                                                                                   |
+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+
| Case 1: AIPED = 0 (Constant Mass Rate, 1- or 2-Phase Source or Sink)                                                                                                               |
+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+
| SKD                                                                      | real   | 0.      | Mass source strength (kg/s). Negative value indicates injection into the rock mass.  |
+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+
| EFLOW                                                                    | real   | 0.      | | a) EFLOW ≥ 0, EFLOW is the source liquid saturation,                               |
|                                                                          |        |         | | * :math:`Q_w = SKD \cdot EFLOW` (kg/s)                                             |
|                                                                          |        |         | | * :math:`Q_a = SKD \cdot (1 - EFLOW)` (kg/s)                                       |
+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+
|                                                                          |        |         | | b) EFLOW < 0, ABS(EFLOW) is the source air pressure (MPa)                          |
|                                                                          |        |         | | * :math:`Q_w = SKD` (kg/s)                                                         |
|                                                                          |        |         | | * :math:`Q_a = 1.0 \cdot (P_a - ABS(EEFLOW))` (kg/s)                               |
+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+
| AIPED                                                                    |        |         | Used only as flag to indicatee Constant Mass Rate                                    |
+--------------------------------------------------------------------------+--------+---------+--------------------------------------------------------------------------------------+


In the above and following relations, :math:`Q_w` is the source term for water, :math:`Q_a` is the source term for air,
and :math:`P_a` is the in-place air pressure. The second case works well in situations where
inflow is specified and it is desired to hold the air pressure at a constant value.


+----------------------------------------------------------------------------------+------+----+---------------------------------------------------------------------------------------------+
| Case 2: AIPED > 0 (Constant Pressure, Constant Liquid Saturation Source or Sink)                                                                                                           |
+----------------------------------------------------------------------------------+------+----+---------------------------------------------------------------------------------------------+
| SKD                                                                              | real | 0. | Specified source pressure (MPa).                                                            |
+----------------------------------------------------------------------------------+------+----+---------------------------------------------------------------------------------------------+
| EFLOW                                                                            | real | 0. | | a) EFLOW < 0, air only source.                                                            |
|                                                                                  |      |    | | * :math:`Q_a = AIPED \cdot (P_a - SKD)` (kg/s)                                            |
|                                                                                  |      |    | |                                                                                           |
|                                                                                  |      |    | | b) 0 < EFLOW < 1, EFLOW is specified source liquid saturation,                            |
|                                                                                  |      |    | | for SKD ≥ 0, 2-phase source,                                                              |
|                                                                                  |      |    | | * :math:`Q_a = AIPED \cdot (P_a - SKD)` (kg/s)                                            |
|                                                                                  |      |    | | * :math:`Q_w = AIPED \cdot (S_l - EEFLOW) \cdot P_0` (kg/s)                               |
|                                                                                  |      |    | | when SKD < 0, water only source :math:`Q_a = 0`.                                          |
|                                                                                  |      |    | |                                                                                           |
|                                                                                  |      |    | | c) EFLOW = 1, water only source.                                                          |
|                                                                                  |      |    | | * :math:`Q_w = AIPED \cdot (P_l - SKD)` kg/s                                              |
+----------------------------------------------------------------------------------+------+----+---------------------------------------------------------------------------------------------+
| AIPED                                                                            | real |    | | Impedance parameter. A large value is recommended (102 - 106) in order to create a flow   |
|                                                                                  |      |    | | term large enough to maintain constant pressure.                                          |
+----------------------------------------------------------------------------------+------+----+---------------------------------------------------------------------------------------------+


+---------------------------------------------------------+-------+----+----------------------------------------------------------------+
| Case 3: AIPED < 0 (Outflow only, if :math:`P_l > SKD`)                                                                                |
+---------------------------------------------------------+-------+----+----------------------------------------------------------------+
| SKD                                                     | real  | 0. | Pressure above which outflow occurs (MPa)                      |
+---------------------------------------------------------+-------+----+----------------------------------------------------------------+
| EFLOW                                                   | real  | 0. | Not used.                                                      |
+---------------------------------------------------------+-------+----+----------------------------------------------------------------+
| AIPED                                                   | real  | 0. | Impedance parameter.                                           |
+                                                         +       +    +----------------------------------------------------------------+
|                                                         |       |    | :math:`Q_w = ABS(AIPED) \cdot R_l / \mu_l(P_l - SKD)` (kg/s)   |
+---------------------------------------------------------+-------+----+----------------------------------------------------------------+

where :math:`R_l` is the water relative peremeability and :math:`\mu_l` is the water viscosity.


+----------------+---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
|                | PARAMETER     |  SKD                                                                                                        | EFLOW                                                      |
+----------------+---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
| Physics Model  | **AIPED\***   | :math:`\ge 0`                                  | :math:`< 0`                                                | :math:`\ge 0`            | :math:`< 0`                     |
+----------------+---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
| Non-isothermal | :math:`> 0`   | Flowing wellbore pressure (MPa)                | Flowing wellbore pressure (MPa) - injection into rock mass | Enthalpy (MJ/kg)         | Temperature (C)                 |
+                +---------------+------------------------------------------------+------------------------------------------------------------+                          +                                 +
|                | :math:`= 0`   | | Flow rate (kg/s)                             | | Flow rate (kg/s)                                         |                          |                                 |
|                |               | | Heat only (MJ/s)                             | | Heat only (MJ/s) - injection into rock mass              |                          |                                 |
+                +---------------+------------------------------------------------+------------------------------------------------------------+                          +                                 +
|                | :math:`< 0`   | Flowing wellbore pressure (MPa) - outflow only | N/A                                                        |                          |                                 |
+----------------+---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
| Isothermal     | :math:`> 0`   | Specified source pressure (MPa)                | Specified source pressure (MPa) - Water only source        | Source liquid saturation | Air only source (used as flag)  |
+                +---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
|                | :math:`= 0`   | Mass source strength (kg/s)                    | Mass source strength (kg/s) - injection into rock mass     | Source liquid saturation | Source air pressure (MPa)       |
+                +---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
|                | :math:`< 0`   | Pressure above which outflow occurs (MPa)      | N/A                                                        | N/A                      | N/A                             |
+----------------+---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+
| \* Impedance parametere                                                                                                                                                                                   |
+----------------+---------------+------------------------------------------------+------------------------------------------------------------+--------------------------+---------------------------------+

The following are examples of flow. In the first example, at node 88, a mass flow of 0.05 kg/s at 25 C
is being withdrawn from the model. Because fluid is being withdrawn the in-place temperature will actually be used.
For every 14th node from node 14 to 140, the pressure and temperature are being held constant at 3.6 MPa and 160 C,
respectively. This represents a constant temperature recharge along one of the problem boundaries.

+------+-----+----+-------+--------+
| flow |     |    |       |        |
+------+-----+----+-------+--------+
| 88   | 88  | 1  | 0.050 | -25.0  |
+------+-----+----+-------+--------+
| 14   | 140 | 14 | 3.600 | -160.0 |
+------+-----+----+-------+--------+


In the second example, the corresponding input for airwater, is included, indicating
an isothermal air-water two-phase simulation is being run with a reference temperature
for property evaluation of 20 C and a reference pressure of 0.1 MPa. At nodes 26 and 52,
water saturation is 100% and water is being injected at 2.e-3 kg/s. At nodes 1 and 27,
there is an air only source, with a specified pressure of 0.1 MPa, and the air is
being injected at the rate of 100\*(Pa - 0.1) kg/s.

+----------+-----+----+--------+------+
| airwater |     |    |        |      |
+----------+-----+----+--------+------+
| 2        |     |    |        |      |
+----------+-----+----+--------+------+
| 20.0     | 0.1 |    |        |      |
+----------+-----+----+--------+------+
| flow     |     |    |        |      |
+----------+-----+----+--------+------+
| 26       | 52  | 26 | -2.e-3 | 1.0  |
+----------+-----+----+--------+------+
| 1        | 27  | 26 | 0.1    | -0.2 |
+----------+-----+----+--------+------+
|          |     |    |        |      |
+----------+-----+----+--------+------+

