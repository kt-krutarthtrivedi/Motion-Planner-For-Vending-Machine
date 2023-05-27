# Motion Planner For Vending Machine

## About the project
The soda starts trapped inside a chamber in the vending machine, and must be maneuvered past two barriers to get outside. The goal of this project is to create an RRT-based motion planner to steal the soda.

## About the environment
The environment consists of the vending machine interior, with the main chamber and two barriers connected. Each barrier has a window, just barely large enough to fit a soda can. These windows are misaligned, as an anti-theft measure that must be defeated. The soda can is a standard 12 oz. aluminum beverage can, modeled as a perfect cylinder with
a diameter of 52 mm and height of 122 mm. The main chamber of the vending machine is a cube 1 meter on a side. The first barrier is on the far wall, with an opening with its center 200 mm from the top. The second barrier is offset 250 mm from the first, with an opening with its center 200 mm from the bottom. Both windows are squares, 150 mm on a side, and aligned with the centerline of the inner chamber, along the axis normal to the barriers. A sample of the environment is shown below:

![147783728-3228e148-a74c-4540-9aa7-6af992a6e64c](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/329432ad-be22-498d-8bb6-3185b0dea577)


## Planners used

The above project has been implemented using the RRT Algorithm. Following is the graph plot from the RRT Planner:


![147785281-67df6eff-bd5f-4a06-b090-efe7f66d5308](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/de3f2efc-50f7-47c5-bba2-7c444a005be2)

&nbsp;

![147785287-f136cfea-a3a6-48a2-bcbc-f041521310af](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/99ff0d7a-e011-4f8e-8a09-b07db97be41c)

&nbsp;

![147785298-b44c2cf0-11cf-4a74-aca0-fd5e235b2c80](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/64ae3cf2-ac7e-444d-b0ae-79d8dda241de)

&nbsp;
&nbsp;

Following are the images of the final path:

![147785244-ed6e3101-d88c-430b-a206-6d992f7fe97d](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/0377bad8-ab3a-4dfa-97ca-d8d2918a825c)

&nbsp;

![147785248-432d9c2f-c7cf-4470-8fa7-3511a161f8a0](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/c75ea328-715d-42ff-b02f-fb9695abed38)

&nbsp;

![147785254-7b49e179-8f25-44f8-a2e4-72c81288e87a](https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/3d636edd-b4c8-42a3-9f3c-2de10ca3a1bd)

&nbsp;


## Demo

https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/7a8ac6ed-dbf6-455e-8cdc-9e4dec0fd744


&nbsp;


https://github.com/kt-krutarthtrivedi/Motion-Planner-For-Vending-Machine/assets/134632027/1840ac83-e1f8-4385-a151-9f8fb5850ba1




## References

* [Steven M. LaValle. Planning Algorithms. Cambridge University Press, May 2006.
9780521862059.](http://lavalle.pl/planning/)


