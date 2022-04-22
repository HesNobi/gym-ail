"""An observation wrapper that augments observations by pixel values."""

import collections
import copy
from collections.abc import MutableMapping

import numpy as np
import OpenGL.GLUT as gl

from gym import ObservationWrapper, spaces

<<<<<<< Updated upstream
STATE_KEY = "state"


class PixelObservationWrapper(ObservationWrapper):
    """Augment observations by pixel values."""

    def __init__(
        self, env, pixels_only=True, render_kwargs=None, pixel_keys=("pixels",)
    ):
        """Initializes a new pixel Wrapper.

        Args:
            env: The environment to wrap.
            pixels_only: If `True` (default), the original observation returned
                by the wrapped environment will be discarded, and a dictionary
                observation will only include pixels. If `False`, the
                observation dictionary will contain both the original
                observations and the pixel observations.
            render_kwargs: Optional `dict` containing keyword arguments passed
                to the `self.render` method.
            pixel_keys: Optional custom string specifying the pixel
                observation's key in the `OrderedDict` of observations.
                Defaults to 'pixels'.

        Raises:
            ValueError: If `env`'s observation spec is not compatible with the
                wrapper. Supported formats are a single array, or a dict of
                arrays.
            ValueError: If `env`'s observation already contains any of the
                specified `pixel_keys`.
        """
=======
class PixelObservationWrapper(ObservationWrapper):
    """Augment observations by pixel values."""

    def __init__(self,
                 env,
                 render_shape=None):

        # Creating a dummy GL Windows to bupas the Error: "GLEW initalization error: Missing GL version"
        gl.glutInit()
        gl.glutInitWindowSize(500, 500)
        gl.glutCreateWindow('GLEW Testing')
>>>>>>> Stashed changes

        super().__init__(env)

<<<<<<< Updated upstream
        if render_kwargs is None:
            render_kwargs = {}

        for key in pixel_keys:
            render_kwargs.setdefault(key, {})

            render_mode = render_kwargs[key].pop("mode", "rgb_array")
            assert render_mode == "rgb_array", render_mode
            render_kwargs[key]["mode"] = "rgb_array"

        wrapped_observation_space = env.observation_space

        if isinstance(wrapped_observation_space, spaces.Box):
            self._observation_is_dict = False
            invalid_keys = {STATE_KEY}
        elif isinstance(wrapped_observation_space, (spaces.Dict, MutableMapping)):
            self._observation_is_dict = True
            invalid_keys = set(wrapped_observation_space.spaces.keys())
        else:
            raise ValueError("Unsupported observation space structure.")

        if not pixels_only:
            # Make sure that now keys in the `pixel_keys` overlap with
            # `observation_keys`
            overlapping_keys = set(pixel_keys) & set(invalid_keys)
            if overlapping_keys:
                raise ValueError(
                    f"Duplicate or reserved pixel keys {overlapping_keys!r}."
                )

        if pixels_only:
            self.observation_space = spaces.Dict()
        elif self._observation_is_dict:
            self.observation_space = copy.deepcopy(wrapped_observation_space)
        else:
            self.observation_space = spaces.Dict()
            self.observation_space.spaces[STATE_KEY] = wrapped_observation_space

        # Extend observation space with pixels.

        pixels_spaces = {}
        for pixel_key in pixel_keys:
            pixels = self.env.render(**render_kwargs[pixel_key])

            if np.issubdtype(pixels.dtype, np.integer):
                low, high = (0, 255)
            elif np.issubdtype(pixels.dtype, np.float):
                low, high = (-float("inf"), float("inf"))
            else:
                raise TypeError(pixels.dtype)

            pixels_space = spaces.Box(
                shape=pixels.shape, low=low, high=high, dtype=pixels.dtype
            )
            pixels_spaces[pixel_key] = pixels_space

        self.observation_space.spaces.update(pixels_spaces)

        self._env = env
        self._pixels_only = pixels_only
        self._render_kwargs = render_kwargs
        self._pixel_keys = pixel_keys
=======
        self.render_shape =render_shape

        pixels = self.render(mode='rgb_array',width=render_shape[0],height=render_shape[1])
        low, high = (0, 255)
        self.observation_space = spaces.Box(shape=pixels.shape, low=low, high=high, dtype=np.uint8)
        self._max_episode_steps = env._max_episode_steps

    def observation(self, observation):
        pixel_observation = self._add_pixel_observation(observation)
        return pixel_observation

    def _add_pixel_observation(self, wrapped_observation):
        return self.render(mode='rgb_array',width=self.render_shape[0],height=self.render_shape[1])


class PixelObservationWrapper_classic(ObservationWrapper):
    """Augment observations by pixel values."""

    def __init__(self,
                 env,
                 render_shape=None):
        raise NotImplementedError

        super(PixelObservationWrapper_classic, self).__init__(env)

        self.render_shape = render_shape

        low, high = (0, 255)
        self.observation_space = spaces.Box(shape=(render_shape[0],render_shape[1],3), low=low, high=high, dtype=np.uint8)
        self._max_episode_steps = env._max_episode_steps
>>>>>>> Stashed changes

    def observation(self, observation):
        pixel_observation = self._add_pixel_observation(observation)
        return pixel_observation

    def _add_pixel_observation(self, wrapped_observation):
        img = self.render('rgb_array')#, width=self.render_shape[0], height=self.render_shape[1])
        return img

